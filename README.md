# Gem → Agent 升級導引包（gem-to-agent-kit）

把你在 **Google Gemini 的 Gem**，升級成可讀檔、可跑程式、可生圖、可批次的 **Agent 工作流**。
主打 **Google Antigravity**（生圖用內建 Nano Banana Pro），同時支援 Codex / Claude Code / OpenCode。

## 這是什麼
一個給 **AI agent 讀**的導引包。你把這個 repo 交給你的 agent，它就會扮演「升級顧問」，帶你：
裝 Google Drive App → 找到 `Gemini Gems` 資料夾 → 唯讀解析你的 Gem → 分類與升級建議 →
（確認後）安裝需要的工具 → 在硬碟建升級版 project → 視需要升級為全域 skill。

## 🚨 隱私警告（務必先讀）
- 本 repo **只放通用工具**。
- **絕對不要**把你自己的 Gem 指令、知識檔（試卷、班級資料等）上傳到 GitHub 或任何公開位置。
- 升級流程全程**唯讀**你的原始 Gem，不會改動原檔。

## 怎麼用
把這個 repo 給你的 agent，並說：「請依 `AGENTS.md` 幫我升級我的 Gem。」

## 內容
```
gem-to-agent-kit/
├── AGENTS.md        agent 入口（流程、安全原則）
├── rubric.md        決策大腦（分類與升級評估標準）
├── deps_matrix.md   相依套件 + 生圖 adapter 對照
├── scripts/         detect_env / find_gem_folder / parse_gem
├── templates/       升級版 project 標準骨架
└── adapters/        各 agent 的生圖方式與全域安裝差異
```

## 支援平台
| Agent | 生圖 | 全域 skill |
|---|---|---|
| Antigravity（主要）| 內建 Nano Banana Pro | `~/.gemini/skills/` |
| Codex | 內建 image 2 | 依 Codex |
| Claude Code | 接 API（gpt-image 等）| `~/.claude/skills/` |
| OpenCode | 接 API | 依 OpenCode |

授權：MIT
