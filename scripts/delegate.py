#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
delegate.py — 把任務派給子 agent（codex / opencode / agy），
把「完整輸出」落地到 log 檔，只回傳一份「精簡摘要」給呼叫者（省 token）。

設計目的：總指揮（如 Claude）不要把子 agent 的整段對話/推理吞進 context。
只看：① 退出碼 ② 改了哪些檔（git diff --stat）③ 最終答案摘要 ④ token/成本 ⑤ log 路徑。

用法：
    python scripts/delegate.py --agent codex   --task "把 README 加一段安裝說明" --dir <repo> --write
    python scripts/delegate.py --agent opencode --task "修好 bug" --dir <repo> --model opencode-go/deepseek-v4-pro
    python scripts/delegate.py --agent agy      --task "在 <dir> 建 X 檔" --dir <ws>

摘要預設只印最終答案的前 N 字（--max-chars 調整）；完整輸出在 log 檔。
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _winwrap(cmd):
    """Windows：把 npm 的 .cmd/.bat、.ps1 包裝檔解析成可被 subprocess 執行的形式。"""
    exe = shutil.which(cmd[0]) or cmd[0]
    low = exe.lower()
    if low.endswith((".cmd", ".bat")):
        return ["cmd", "/c", exe] + cmd[1:]
    if low.endswith(".ps1"):
        return ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", exe] + cmd[1:]
    return [exe] + cmd[1:]


def _run(cmd, cwd, log_path):
    """執行子 agent，stdin 關閉（避免卡等），全文寫入 log 檔。回傳 (exit_code, full_text)。"""
    cmd = _winwrap(cmd)
    with open(log_path, "w", encoding="utf-8") as f:
        proc = subprocess.run(
            cmd, cwd=cwd, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace",
        )
        f.write(proc.stdout or "")
    return proc.returncode, (proc.stdout or "")


def _git_changes(dir_):
    """回傳 git diff --stat 與 porcelain（只看改了哪些檔，不讀內容）。非 git repo 回 None。"""
    try:
        inside = subprocess.run(["git", "-C", dir_, "rev-parse", "--is-inside-work-tree"],
                                capture_output=True, text=True)
        if inside.returncode != 0:
            return None
        stat = subprocess.run(["git", "-C", dir_, "diff", "--stat"],
                              capture_output=True, text=True).stdout.strip()
        untracked = subprocess.run(["git", "-C", dir_, "status", "--porcelain"],
                                   capture_output=True, text=True).stdout.strip()
        return (stat, untracked)
    except Exception:
        return None


def _recent_files(dir_, since_sec=180):
    """非 git repo 的後備：列出近期被修改的檔。"""
    now = time.time()
    out = []
    for p in Path(dir_).rglob("*"):
        if p.is_file() and (now - p.stat().st_mtime) <= since_sec:
            out.append(str(p.relative_to(dir_)))
    return out[:20]


def _extract_answer(agent, text, max_chars):
    """從全文抽出『最終答案』，丟掉推理/工具日誌。"""
    if agent == "opencode":
        # --format json：逐行 JSON 事件，取最後的 assistant 文字 + cost
        answer, cost = "", None
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
            except Exception:
                continue
            # 盡量相容不同事件結構
            if isinstance(ev, dict):
                if ev.get("cost") is not None:
                    cost = ev.get("cost")
                for key in ("text", "content", "message", "result"):
                    v = ev.get(key)
                    if isinstance(v, str) and v.strip():
                        answer = v
        tail = answer or "(未解析到 assistant 文字，請看 log)"
        if cost is not None:
            tail += f"\n[cost: {cost}]"
        return tail[:max_chars]

    if agent == "codex":
        # 取最後一個 'codex' 標記後、'tokens used' 前的內容；失敗則取尾部
        lines = text.splitlines()
        ans = []
        capture = False
        for ln in lines:
            s = ln.strip()
            if s == "codex":
                capture, ans = True, []
                continue
            if "tokens used" in s.lower():
                capture = False
                continue
            if capture and s:
                ans.append(s)
        result = "\n".join(ans).strip() if ans else "\n".join(
            [l for l in lines if l.strip()][-8:])
        return result[:max_chars]

    # agy：沒有純文字輸出
    return "(agy 無 stdout；請以下方檔案變更為準)"


def _build_cmd(agent, task, dir_, model, write):
    if agent == "codex":
        sandbox = "workspace-write" if write else "read-only"
        return ["codex", "exec", "--sandbox", sandbox, "--skip-git-repo-check", task]
    if agent == "opencode":
        cmd = ["opencode", "run", "--format", "json", "--dir", dir_]
        if model:
            cmd[2:2] = ["-m", model]  # 插在 run 之後
        cmd.append(task)
        return cmd
    if agent == "agy":
        agy_bin = os.path.expandvars(r"%LOCALAPPDATA%\agy\bin\agy.exe")
        agy_exe = agy_bin if os.path.exists(agy_bin) else "agy"
        return [agy_exe, "-p", task, "--add-dir", dir_, "--dangerously-skip-permissions"]
    raise SystemExit(f"未知 agent：{agent}")


def main():
    ap = argparse.ArgumentParser(description="派任務給子 agent，只回精簡摘要（省 token）")
    ap.add_argument("--agent", required=True, choices=["codex", "opencode", "agy"])
    ap.add_argument("--task", required=True)
    ap.add_argument("--dir", required=True, help="工作區（也是 cwd）")
    ap.add_argument("--model", default=None, help="opencode 用的模型 id")
    ap.add_argument("--write", action="store_true", help="允許子 agent 寫檔（codex 用 workspace-write）")
    ap.add_argument("--max-chars", type=int, default=600, help="摘要最多字數")
    args = ap.parse_args()

    dir_ = str(Path(args.dir).resolve())
    Path(dir_).mkdir(parents=True, exist_ok=True)
    log_path = Path(dir_) / f"_delegate_{args.agent}.log"

    cmd = _build_cmd(args.agent, args.task, dir_, args.model, args.write)
    t0 = time.time()
    code, full = _run(cmd, dir_, log_path)
    dt = round(time.time() - t0, 1)

    answer = _extract_answer(args.agent, full, args.max_chars)
    changes = _git_changes(dir_)

    # ===== 精簡摘要（這才是回給呼叫者的東西）=====
    print(f"=== delegate 摘要 ===")
    print(f"agent: {args.agent} | exit: {code} | 耗時: {dt}s")
    if changes is not None:
        stat, porcelain = changes
        print("檔案變更 (git diff --stat):")
        print(stat or "  (工作區無 tracked 變更)")
        if porcelain:
            print("未追蹤/狀態 (porcelain):")
            print(porcelain)
    else:
        print("檔案變更 (近 3 分鐘修改):")
        rf = _recent_files(dir_)
        print("\n".join(f"  {x}" for x in rf) if rf else "  (無)")
    print("最終答案摘要:")
    print(answer)
    print(f"[完整輸出 log: {log_path}]")


if __name__ == "__main__":
    main()
