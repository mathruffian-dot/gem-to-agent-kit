# 多 CLI 指揮與省 token 規範（ORCHESTRATION）

總指揮（如 Claude）遙控子 agent（codex / opencode / agy）時，**不要把子 agent 的整段對話/推理讀進自己的 context**——又貴又髒。一律透過 `scripts/delegate.py`。

## 核心原則
1. **全文落地、只回摘要**：子 agent 的完整輸出寫到 `_delegate_<agent>.log`；呼叫者只看 delegate 印出的 10 行摘要。
2. **看交付物，不看話術**：用 `git diff --stat` 知道「改了哪些檔」，需要時才讀特定檔內容。
3. **輸出契約**：派工時要求子 agent 把產物放指定路徑；必要時叫它寫一個 `RESULT.md`（≤10 行：做了什麼、改了哪些檔、結果）。

## 用法
```bash
# 問答 / 唯讀（不改檔）
python scripts/delegate.py --agent codex --task "..." --dir <repo>

# 允許改檔
python scripts/delegate.py --agent codex --task "..." --dir <repo> --write
python scripts/delegate.py --agent opencode --task "..." --dir <repo> --model opencode-go/deepseek-v4-pro
python scripts/delegate.py --agent agy --task "在 <dir> 建/改某檔" --dir <ws>
```

## delegate 回傳的摘要長相
```
=== delegate 摘要 ===
agent: codex | exit: 0 | 耗時: 6.2s
檔案變更 (git diff --stat):
 README.md | 4 ++++
最終答案摘要:
已加入安裝說明段落。
[完整輸出 log: <dir>/_delegate_codex.log]
```

## 各 agent 擷取方式
| agent | 答案來源 | 備註 |
|---|---|---|
| codex | stdout 最後 `codex` 區塊 | 能擷取回答；`--write` 改檔 |
| opencode | `--format json` 解析最終訊息 + cost | 能擷取回答 |
| agy | **無 stdout** → 看 git diff / RESULT.md | 只能靠檔案副作用驗收 |

## 缺點與緩解（尤其 agy）
- agy 看不到推理、可能靜默失敗（exit 0 ≠ 成功）→ **每次都 git diff 驗收**、`--add-dir` 範圍縮到最小、要求寫 `RESULT.md`。
- 長任務無串流 → 切小任務。

> `_delegate_*.log` 與 `RESULT.md` 已建議列入 `.gitignore`，避免把子 agent 產物推上版控。
