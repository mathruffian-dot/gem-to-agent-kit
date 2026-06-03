# Adapter：Google Antigravity（主要對象）

## 生圖
- 方式：**內建 Nano Banana Pro**，直接呼叫，無需 API 金鑰。
- 額度：吃使用者訂閱的生圖配額池（與 Gemini App 每日額度、開發者 API 皆獨立）。
- 抽象指令對應：Skill 寫「產生一張圖：<描述>」→ 由 Agent 內建生圖工具產出到 `output/`。
- 角色一致（漫畫/繪本）：先生「角色三視圖參考表」，後續逐格帶入參考圖；同場景角色 ≤ 5。

## Skill / workflow 位置
- 工作區：`<project>/.agents/skills/<name>/SKILL.md`、`<project>/.agents/workflows/<name>.md`
- 全域：`~/.gemini/skills/<name>/SKILL.md`

## 全域升級流程
先建工作區 skill → 測試 → 詢問使用者 → 確認後複製到 `~/.gemini/skills/`。

## 備註
- 這是本 kit 的第一級目標：範本與優化都以 Antigravity 為準。
