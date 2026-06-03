# Adapter：Codex

## 生圖
- 方式：**內建 image 2（gpt-image-2）**，用 Codex 內建生圖，無需另接 API。
- 抽象指令對應：Skill 寫「產生一張圖：<描述>」→ 由 Codex 內建生圖產出到 `output/`。

## Skill / 全域
- 依 Codex 的設定慣例放置；全域位置請依當前 Codex 版本文件確認後再寫入。

## 備註
- 若 Codex 內建生圖不可用，退回「外部 API」做法（見 claude.md / opencode.md）。
