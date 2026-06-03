# 升級版 project 標準骨架

複製這個資料夾當作每個「Gem 升級版」的起點。

```
<專案名稱>/
├── AGENTS.md                  固定偏好
├── .agents/
│   ├── skills/<name>/SKILL.md  凍住的流程
│   └── workflows/<name>.md      一鍵觸發
├── scripts/                   這個流程要呼叫的 Python（需要算的事都放這）
├── input/                     【每次換這裡】材料
└── output/                    產出成品
```

原則：**固定流程＋規格放 Skill / scripts，浮動材料放 input/。**
