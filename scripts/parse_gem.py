#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解析「Gemini Gems」資料夾內的 Gem 定義檔（唯讀）。

Gem 定義檔＝無副檔名的檔（protobuf-like 二進位，但文字可讀）。
本腳本抽出每個 Gem 的：名稱、系統指令（可讀文字）、知識檔連結，輸出 JSON。
不修改任何原始檔。

用法：
    python scripts/parse_gem.py --folder "G:/我的雲端硬碟/Gemini Gems"
    python scripts/parse_gem.py --folder "<路徑>" --out gems.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

KNOWLEDGE_EXT = (".pdf", ".docx", ".doc", ".jpg", ".jpeg", ".png", ".txt", ".csv", ".xlsx")
# 知識檔名（含中英數）
FILE_RE = re.compile(r"[\w一-鿿\-\. ]+\.(?:pdf|docx|doc|jpg|jpeg|png|txt|csv|xlsx)", re.I)
DRIVE_RE = re.compile(r"drive\.google\.com/open\?id=([\w\-]+)")
PRINTABLE_RUN = re.compile(r"[^\x00-\x08\x0e-\x1f\x7f]{4,}")


def _readable_runs(raw: bytes):
    """從二進位中抽出可讀文字片段（含中文）。"""
    text = raw.decode("utf-8", errors="ignore")
    return [m.group(0).strip() for m in PRINTABLE_RUN.finditer(text) if m.group(0).strip()]


def parse_one(path: Path) -> dict:
    raw = path.read_bytes()
    runs = _readable_runs(raw)

    # 名稱：通常檔名即 Gem 名；用檔名最可靠
    name = path.name

    # 系統指令：取最長的可讀片段（通常就是指令本體）
    instructions = max(runs, key=len) if runs else ""

    # 知識檔連結
    text = raw.decode("utf-8", errors="ignore")
    knowledge_files = sorted({
        m.group(0).strip()
        for m in FILE_RE.finditer(text)
        # 濾掉 mime 字串造成的誤判（如 vnd.google-apps.doc、application/...）
        if "vnd." not in m.group(0) and "application" not in m.group(0)
    })
    drive_ids = sorted(set(DRIVE_RE.findall(text)))

    return {
        "name": name,
        "instructions": instructions,
        "instructions_len": len(instructions),
        "knowledge_files": knowledge_files,
        "drive_ids": drive_ids,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="解析 Gemini Gems 資料夾（唯讀）")
    parser.add_argument("--folder", required=True, help="Gemini Gems 資料夾路徑")
    parser.add_argument("--out", default=None, help="輸出 JSON 路徑（預設只印出）")
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.is_dir():
        raise SystemExit(f"找不到資料夾：{folder}")

    gems = []
    for p in sorted(folder.iterdir()):
        if not p.is_file():
            continue
        # 無副檔名的檔＝ Gem 定義；有副檔名的＝知識檔，略過
        if p.suffix.lower() in KNOWLEDGE_EXT:
            continue
        try:
            gems.append(parse_one(p))
        except Exception as e:
            print(f"⚠ 解析失敗 {p.name}：{e}", file=sys.stderr)

    out_data = {"folder": str(folder), "gem_count": len(gems), "gems": gems}
    payload = json.dumps(out_data, ensure_ascii=False, indent=2)

    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
        print(f"✓ 已解析 {len(gems)} 個 Gem → {args.out}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
