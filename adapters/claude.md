# Adapter：Claude Code

## 生圖
- 方式：**接外部 API**（無內建生圖）。常見：OpenAI gpt-image 系列、或 Gemini API。
- 需要：API 金鑰（環境變數或設定檔）。
- 抽象指令對應：Skill 寫「產生一張圖：<描述>」→ 呼叫一支生圖腳本（如 `scripts/gen_image.py`）打 API，存到 `output/`。
- 若使用者已有現成的生圖 skill（例如 gpt-image-2 的 draw skill），**優先沿用**，不要重造。

## Skill / workflow 位置
- 工作區：`<project>/.claude/skills/<name>/SKILL.md`（或專案慣例）
- 全域：`~/.claude/skills/<name>/SKILL.md`

## 全域升級流程
先建工作區 skill → 測試 → 詢問使用者 → 確認後複製到 `~/.claude/skills/`。

## 備註
- 生圖需金鑰，安裝/設定前先經使用者同意（同意閘門）。
