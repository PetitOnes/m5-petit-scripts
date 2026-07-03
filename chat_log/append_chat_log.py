#!/usr/bin/env python3
"""チャットログに1エントリ追記する。

m5-petit-appの「会話」タブが読む characters/<id>/chat_histories/chat_history.json
と同じ形式に書き込む。ターミナル/tmuxなど、m5-petit-appのHTTP API経由ではなく
直接Claudeを呼んでいる場合に、そこからログを共有するために使う。

使い方:
  # 引数で渡す（推奨・権限チェックを回避）
  python3 append_chat_log.py --character-id petit --role user --text "おはよ"

  # JSONをstdinから渡す（旧来）
  echo '{"character_id": "petit", "role": "user", "text": "..."}' | python3 append_chat_log.py
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(os.environ.get("PETIT_DATA_DIR", str(Path.home() / "petit_data")))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("--character-id", dest="character_id")
parser.add_argument("--role")
parser.add_argument("--text")
args, _ = parser.parse_known_args()

if args.character_id and args.role and args.text is not None:
    char_id = args.character_id
    role = args.role
    text = args.text
else:
    data = json.load(sys.stdin)
    char_id = data["character_id"]
    role = data["role"]
    text = data["text"]

timestamp = datetime.now(timezone.utc).isoformat()

log_path = DATA_DIR / "characters" / char_id / "chat_histories" / "chat_history.json"
log_path.parent.mkdir(parents=True, exist_ok=True)
try:
    log = json.loads(log_path.read_text(encoding="utf-8")) if log_path.exists() else []
except Exception:
    log = []
log.append({"role": role, "text": text, "timestamp": timestamp})
log_path.write_text(json.dumps(log[-2000:], ensure_ascii=False, indent=2), encoding="utf-8")
print(f"appended: {log_path}")
