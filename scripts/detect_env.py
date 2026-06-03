#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
環境偵測：回報 OS、語言、已裝的 runtime 與 Python 套件。
輸出 JSON，供 agent 判斷要不要安裝相依工具。

用法：
    python scripts/detect_env.py
"""

import json
import locale
import platform
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 要偵測的命令列工具
CLI_TOOLS = ["python", "python3", "node", "npm", "git", "ffmpeg", "yt-dlp", "netlify", "edge-tts"]
# 要偵測的 Python 套件
PY_PACKAGES = ["docx", "openpyxl", "PIL", "pptx", "edge_tts", "yt_dlp"]


def _check_cli(tools):
    return {t: bool(shutil.which(t)) for t in tools}


def _check_python_pkgs(pkgs):
    import importlib.util
    result = {}
    for p in pkgs:
        result[p] = importlib.util.find_spec(p) is not None
    return result


def main() -> None:
    try:
        lang = locale.getlocale()[0] or locale.getdefaultlocale()[0]
    except Exception:
        lang = None

    report = {
        "os": platform.system(),          # Windows / Darwin / Linux
        "os_release": platform.release(),
        "language": lang,
        "python_version": platform.python_version(),
        "cli_tools": _check_cli(CLI_TOOLS),
        "python_packages": _check_python_pkgs(PY_PACKAGES),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
