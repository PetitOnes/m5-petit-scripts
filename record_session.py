#!/usr/bin/env python3
"""
インタラクティブセッション終了時に、話した時刻を記録するスクリプト。
Claude Codeの Stop フックから呼び出す想定。

環境変数:
  PETIT_CHARACTER_ID  キャラクターID（デフォルト: petit）
  PETIT_SESSION_USER  セッション相手のユーザー名（省略可）
  PETIT_DATA_DIR      データディレクトリ（デフォルト: ~/petit_data）
"""
import os
import sys
from datetime import datetime
from pathlib import Path

CHARACTER_ID = os.environ.get("PETIT_CHARACTER_ID", "petit")
SESSION_USER = os.environ.get("PETIT_SESSION_USER", "")
DATA_DIR = Path(os.environ.get("PETIT_DATA_DIR", str(Path.home() / "petit_data")))
char_dir = DATA_DIR / "characters" / CHARACTER_ID
state_dir = char_dir / "state"
last_session_file = state_dir / "last_session.txt"

if not char_dir.exists():
    sys.exit(0)

state_dir.mkdir(parents=True, exist_ok=True)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
line = f"{now} {SESSION_USER}".strip() + "\n"
last_session_file.write_text(line)
