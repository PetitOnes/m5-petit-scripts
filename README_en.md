# m5-petit-scripts

## [日本語ページ](./README.md)

A collection of general-purpose utility scripts for M5 Petit. Firmware (`.ino`) also lives here (coming soon).

Every script operates on data under `$PETIT_DATA_DIR` (default `~/petit_data`), using the same directory layout as [m5-petit-app](https://github.com/PetitOnes/m5-petit-app) (`characters/<character_id>/chat_histories/`, `characters/<character_id>/stream_logs/`, etc.).

## Scripts

### Mailbox

- `mark_mail_read.py <character_id> <filename...>` / `--all` — mark mail as read
- `list_unread_mail.py <character_id>` — list unread mail

### Chat log / records

For sharing logs when calling Claude directly (e.g. from a terminal) instead of through m5-petit-app's HTTP API.

- `append_chat_log.py --character-id <id> --role <role> --text <text>` — append one entry to the chat log (used by the "Chat" tab)
- `save_chat_stream_log.py` — save a stream-json transcript (used by the "Records" tab). Takes JSON via stdin or a file argument
- `read_stream.py <file or character_id>` — pretty-print a stream-json log with colors
- `format_stream_log.py [file]` — pipe stream-json in, get a plain-text log out

### Cost tracking

- `generate_cost_summary.py [--budget USD] [--reset-day N]` — aggregate cost from `characters/*/stream_logs/` and write a Markdown summary

### Voice

- `register_tts_voices.py --chars <id...> --tts-url <url> --asr-url <url>` — generate TTS voice samples for each character and register them for speaker recognition (ASR)

## Environment variables

| Variable | Description | Default |
| --- | --- | --- |
| `PETIT_DATA_DIR` | Data directory (shared with m5-petit-app) | `~/petit_data` |
| `TTS_URL` / `ASR_URL` | TTS/ASR server URLs (for `register_tts_voices.py`) | — |
