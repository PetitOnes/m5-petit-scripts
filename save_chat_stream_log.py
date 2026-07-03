#!/usr/bin/env python3
"""ターミナルチャットのstream-jsonログを保存する。

m5-petit-appの「記録」タブが読む characters/<id>/stream_logs/*.jsonl と
同じ形式で書き込む。Claudeが各ターン後にBashから呼ぶ想定。

入力: JSONファイルパス（引数）またはstdin
入力JSON形式:
{
  "character_id": "petit",
  "thinking": "思考内容（省略可）",
  "tools": [
    {"name": "ツール名", "input": {省略可}, "output": "結果テキスト"},
    ...
  ],
  "response": "最終返答テキスト"
}
出力: $PETIT_DATA_DIR/characters/{char_id}/stream_logs/YYYYMMDD_HHMMSS_terminal_chat.jsonl
"""
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(os.environ.get("PETIT_DATA_DIR", str(Path.home() / "petit_data")))

# 入力読み込み
if len(sys.argv) > 1:
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
else:
    data = json.load(sys.stdin)

char_id = data.get("character_id", "unknown")
thinking = data.get("thinking", "")
tools = data.get("tools", [])
response = data.get("response", "")

# 出力先
now = datetime.now(timezone.utc).astimezone()
log_dir = DATA_DIR / "characters" / char_id / "stream_logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / f"{now.strftime('%Y%m%d_%H%M%S')}_terminal_chat.jsonl"

session_id = str(uuid.uuid4())
lines = []

def add(obj):
    obj["session_id"] = session_id
    lines.append(json.dumps(obj, ensure_ascii=False))

# thinking
if thinking:
    add({
        "type": "assistant",
        "message": {
            "role": "assistant",
            "content": [{"type": "thinking", "thinking": thinking}]
        }
    })

# tool calls & results
for tool in tools:
    tool_id = str(uuid.uuid4())[:8]
    add({
        "type": "assistant",
        "message": {
            "role": "assistant",
            "content": [{
                "type": "tool_use",
                "id": tool_id,
                "name": tool.get("name", ""),
                "input": tool.get("input", {})
            }]
        }
    })
    add({
        "type": "user",
        "message": {
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_id,
                "content": [{"type": "text", "text": str(tool.get("output", ""))}]
            }]
        }
    })

# final response
if response:
    add({
        "type": "assistant",
        "message": {
            "role": "assistant",
            "content": [{"type": "text", "text": response}]
        }
    })

# result
add({
    "type": "result",
    "subtype": "success",
    "is_error": False,
    "result": response,
    "num_turns": len(tools) + 1,
    "source": "terminal_chat"
})

log_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"saved: {log_file.name}")
