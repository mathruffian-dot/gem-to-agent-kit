# deps_matrix.md — 相依套件 + 生圖 adapter 對照

## 一、相依套件對照（依 Gem 類型）
| Gem 類型 | 需要的工具 | 偵測指令 | 安裝 |
|---|---|---|---|
| 字幕生成 | ffmpeg + whisper/groq | `ffmpeg -version` | 見各 OS |
| 影片下載/摘要 | yt-dlp + ffmpeg | `yt-dlp --version` | `pip install yt-dlp` |
| 解謎生圖 | python + pillow | `python -c "import PIL"` | `pip install pillow` |
| 數學備課/出題 | python-docx + openpyxl | `python -c "import docx,openpyxl"` | `pip install python-docx openpyxl` |
| 簡報 | python-pptx / Marp CLI | `python -c "import pptx"` | `pip install python-pptx` |
| TTS | edge-tts | `edge-tts --version` | `pip install edge-tts` |
| 部署 | netlify-cli | `netlify --version` | `npm i -g netlify-cli` |

**規則**：偵測 → 缺才提示 → 使用者確認 → 才安裝。

### ffmpeg 各 OS 安裝
- Windows：`winget install Gyan.FFmpeg` 或 `choco install ffmpeg`
- macOS：`brew install ffmpeg`
- Linux：`sudo apt install ffmpeg`

## 二、生圖 adapter（依 agent 切換）
Skill 內的生圖步驟一律寫成抽象指令「**產生一張圖：<描述>**」，由 adapter 對應到實際呼叫。

| Agent | 生圖方式 | 是否需 API 金鑰 |
|---|---|---|
| **Antigravity（主要）** | 內建 Nano Banana Pro | 否（吃訂閱配額池）|
| Codex | 內建 image 2（gpt-image-2）| 否 |
| Claude Code | 外部 API（OpenAI gpt-image / Gemini API）| 是 |
| OpenCode | 外部 API | 是 |

詳細各 agent 寫法見 `adapters/`。
