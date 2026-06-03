# Adapter：OpenCode

## 生圖
- 方式：**接外部 API**（無內建生圖），同 Claude Code。
- 需要：API 金鑰。
- 抽象指令對應：Skill 寫「產生一張圖：<描述>」→ 呼叫生圖腳本打 API，存到 `output/`。

## Skill / 全域
- 依 OpenCode 設定慣例放置；全域位置請依當前 OpenCode 文件確認。

## 備註
- 金鑰設定前先經使用者同意。
