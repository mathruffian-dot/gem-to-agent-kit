#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨 OS / 語言 定位 Google Drive 的「Gemini Gems」資料夾。

策略：資料夾名「Gemini Gems」固定，但上層（我的雲端硬碟 / My Drive）與掛載點會變。
本腳本掃描各平台常見的雲端硬碟根目錄，找出底下的 Gemini Gems。

用法：
    python scripts/find_gem_folder.py
找不到時，請使用者手動提供路徑。
"""

import glob
import json
import os
import platform
import string
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

GEM_DIR = "Gemini Gems"
# 上層雲端硬碟資料夾的語言變體
DRIVE_ROOT_NAMES = ["我的雲端硬碟", "My Drive"]


def _candidates_windows():
    cands = []
    # 掃所有磁碟機代號下的「<drive>:\<我的雲端硬碟|My Drive>\Gemini Gems」
    for letter in string.ascii_uppercase:
        for root in DRIVE_ROOT_NAMES:
            cands.append(f"{letter}:\\{root}\\{GEM_DIR}")
    # 使用者家目錄下的可能位置
    home = Path.home()
    for root in DRIVE_ROOT_NAMES:
        cands.append(str(home / root / GEM_DIR))
    return cands


def _candidates_macos():
    home = Path.home()
    cands = []
    # ~/Library/CloudStorage/GoogleDrive-*/My Drive/Gemini Gems
    base = home / "Library" / "CloudStorage"
    for d in glob.glob(str(base / "GoogleDrive-*")):
        for root in DRIVE_ROOT_NAMES:
            cands.append(str(Path(d) / root / GEM_DIR))
    # 舊版 ~/Google Drive/My Drive/Gemini Gems
    for root in DRIVE_ROOT_NAMES:
        cands.append(str(home / "Google Drive" / root / GEM_DIR))
        cands.append(str(home / "Google Drive" / GEM_DIR))
    return cands


def _candidates_linux():
    home = Path.home()
    cands = []
    for base in [home, home / "GoogleDrive", home / "google-drive", Path("/mnt")]:
        for root in DRIVE_ROOT_NAMES + [""]:
            p = base / root / GEM_DIR if root else base / GEM_DIR
            cands.append(str(p))
    return cands


def main() -> None:
    system = platform.system()
    if system == "Windows":
        cands = _candidates_windows()
    elif system == "Darwin":
        cands = _candidates_macos()
    else:
        cands = _candidates_linux()

    found = [c for c in cands if os.path.isdir(c)]
    result = {
        "os": system,
        "found": found,
        "searched": len(cands),
        "hint": "若 found 為空，請使用者手動提供 Gemini Gems 資料夾完整路徑。",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
