#!/usr/bin/env python3
"""交換ノートにエントリを書き込むスクリプト。

m5-petit-appの「ノート」タブが読む notebook/<user_id>/notebook.json に書き込む。

Usage:
    python3 write_notebook.py <author> <content>
    python3 write_notebook.py <author> --file <path>

例:
    python3 write_notebook.py petit "今日はいい天気だった"
    python3 write_notebook.py user --file /tmp/entry.txt

USER_ID環境変数でどのユーザーのノートに書くか指定する（デフォルト: user）。
authorはエントリの書き手を示す自由記述（キャラクター名・ユーザー名どちらでも可）。
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(os.getenv("PETIT_DATA_DIR", str(Path.home() / "petit_data")))
USER_ID = os.getenv("USER_ID", "user")
NOTEBOOK_FILE = DATA_DIR / "notebook" / USER_ID / "notebook.json"


def main() -> int:
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <author> <content>", file=sys.stderr)
        print(f"       {sys.argv[0]} <author> --file <path>", file=sys.stderr)
        return 1

    author = sys.argv[1]

    if sys.argv[2] == "--file" and len(sys.argv) >= 4:
        file_path = Path(sys.argv[3])
        if not file_path.exists():
            print(f"Error: file not found: {file_path}", file=sys.stderr)
            return 1
        content = file_path.read_text(encoding="utf-8")
    else:
        content = " ".join(sys.argv[2:])

    if not content.strip():
        print("Error: content is empty", file=sys.stderr)
        return 1

    NOTEBOOK_FILE.parent.mkdir(parents=True, exist_ok=True)

    if NOTEBOOK_FILE.exists():
        try:
            entries = json.loads(NOTEBOOK_FILE.read_text(encoding="utf-8"))
        except Exception:
            entries = []
    else:
        entries = []

    now = datetime.now(timezone.utc).astimezone()
    entries.append({
        "author": author,
        "date": now.strftime("%Y/%m/%d %H:%M"),
        "content": content.strip(),
    })

    NOTEBOOK_FILE.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"書きました ({author}, {now.strftime('%H:%M')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
