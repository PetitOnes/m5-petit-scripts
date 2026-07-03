# m5-petit-scripts

## [日本語ページ](./README.md)

A collection of general-purpose utility scripts for M5 Petit. Firmware (`.ino`) also lives here (coming soon).

M5Stack CoreS3 firmware will live in [`m5_core_s3_script/`](./m5_core_s3_script/). See [HOW_TO_SETUP_M5_CORES3.md](./HOW_TO_SETUP_M5_CORES3.md) (Japanese) for setup steps.

Every script operates on data under `$PETIT_DATA_DIR` (default `~/petit_data`), using the same directory layout as [m5-petit-app](https://github.com/PetitOnes/m5-petit-app) (`characters/<character_id>/chat_histories/`, `characters/<character_id>/stream_logs/`, etc.).

## Scripts

### `mailbox/`

- `mark_mail_read.py <character_id> <filename...>` / `--all` — mark mail as read
- `list_unread_mail.py <character_id>` — list unread mail

### `chat_log/`

For sharing logs when calling Claude directly (e.g. from a terminal) instead of through m5-petit-app's HTTP API.

- `append_chat_log.py --character-id <id> --role <role> --text <text>` — append one entry to the chat log (used by the "Chat" tab)
- `save_chat_stream_log.py` — save a stream-json transcript (used by the "Records" tab). Takes JSON via stdin or a file argument
- `read_stream.py <file or character_id>` — pretty-print a stream-json log with colors
- `format_stream_log.py [file]` — pipe stream-json in, get a plain-text log out

### `cost/`

- `generate_cost_summary.py [--budget USD] [--reset-day N]` — aggregate cost from `characters/*/stream_logs/` and write a Markdown summary

### `voice/`

- `register_tts_voices.py --chars <id...> --tts-url <url> --asr-url <url>` — generate TTS voice samples for each character and register them for speaker recognition (ASR)

### `notebook/`

- `write_notebook.py <author> <content>` / `--file <path>` — append an entry to the exchange notebook (used by the "Notebook" tab)

### `terminal_chat/`

Scripts for managing a session where you talk to Claude directly in tmux, separate from m5-petit-app's HTTP API.

- `start_chat_session.sh <char_id> <system_prompt_file>` — launch Claude with session resume (with a daily reset). Bring your own system_prompt_file
- `tmux_chat_capture.py --char-id <id>` — extract Claude's replies from `tmux pipe-pane` output and save them to chat_history.json
- `record_session.py` — record when a session ended (meant to be called from a Claude Code Stop hook)

## Environment variables

| Variable | Description | Default |
| --- | --- | --- |
| `PETIT_DATA_DIR` | Data directory (shared with m5-petit-app) | `~/petit_data` |
| `USER_ID` | User ID that determines where notes are saved (for `write_notebook.py`) | `user` |
| `TTS_URL` / `ASR_URL` | TTS/ASR server URLs (for `register_tts_voices.py`) | — |
| `PETIT_CHARACTER_ID` / `PETIT_SESSION_USER` | For `record_session.py` | `petit` / — |
| `PROJECT_DIR` | Used by `start_chat_session.sh` to locate Claude Code's session storage | current directory |
