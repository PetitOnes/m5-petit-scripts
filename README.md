# m5-petit-scripts

## [EnglishPage](./README_en.md)

M5 Petit用の汎用ユーティリティスクリプト集です。ファームウェア(.ino)もここに置きます(準備中)。

いずれのスクリプトも`$PETIT_DATA_DIR`(デフォルト`~/petit_data`)配下のデータを扱い、[m5-petit-app](https://github.com/PetitOnes/m5-petit-app)と同じディレクトリ構成(`characters/<character_id>/chat_histories/`、`characters/<character_id>/stream_logs/`など)を読み書きします。

## スクリプト一覧

### `m5_core_s3_script/` — ファームウェア

M5Stack CoreS3用ファームウェア(.ino)を置く場所です。🚧 現在準備中(まだファイルは入っていません)。

セットアップ手順は[HOW_TO_SETUP_M5_CORES3.md](./HOW_TO_SETUP_M5_CORES3.md)を参照してください(PlatformIOでのビルド・書き込み手順)。

🎬 ブラウザ([Web Flasher](https://petitones.github.io/m5-petit-scripts/))からインストールする様子はこちら → [インストール動画](./videos/install_via_webpage.mp4)

### `mailbox/` — メールボックス

- `mark_mail_read.py <character_id> <filename...>` / `--all` — メールを既読にする
- `list_unread_mail.py <character_id>` — 未読メール一覧を表示

### `chat_log/` — チャットログ・記録

m5-petit-appのHTTP API経由ではなく、ターミナル等から直接Claudeを呼ぶ場合にログを共有するためのスクリプトです。

- `append_chat_log.py --character-id <id> --role <role> --text <text>` — 会話ログ(「会話」タブ用)に1件追記
- `save_chat_stream_log.py` — stream-json形式のログ(「記録」タブ用)を保存。JSON入力(stdinまたはファイル引数)
- `read_stream.py <file or character_id>` — stream-jsonログを色付きで読みやすく表示
- `format_stream_log.py [file]` — stream-jsonをパイプで受けてプレーンテキストログに変換

### `cost/` — コスト集計

- `generate_cost_summary.py [--budget USD] [--reset-day N]` — `characters/*/stream_logs/`からコストを集計し、Markdownサマリーを書き出す

### `voice/` — 音声

- `register_tts_voices.py --chars <id...> --tts-url <url> --asr-url <url>` — キャラのTTS音声を生成して話者認識(ASR)に登録

### `notebook/` — ノート

- `write_notebook.py <author> <content>` / `--file <path>` — 交換ノート(「ノート」タブ用)にエントリを追記

### `terminal_chat/` — ターミナルチャット

tmux上でClaudeと直接対話するセッションを管理するためのスクリプトです(m5-petit-appのHTTP APIとは別の入口)。

- `start_chat_session.sh <char_id> <system_prompt_file>` — セッションIDを引き継いでClaudeを起動(日次リセットつき)。system_prompt_fileは自分で用意してください
- `tmux_chat_capture.py --char-id <id>` — `tmux pipe-pane`の出力からClaudeの返答を抽出してchat_history.jsonに保存
- `record_session.py` — セッション終了時刻を記録(Claude CodeのStopフックから呼ぶ想定)

## 環境変数

| 変数名 | 説明 | デフォルト |
| --- | --- | --- |
| `PETIT_DATA_DIR` | データディレクトリ(m5-petit-appと共有) | `~/petit_data` |
| `USER_ID` | ノートの保存先を決めるユーザーID(`write_notebook.py`用) | `user` |
| `TTS_URL` / `ASR_URL` | TTS/ASRサーバーのURL(`register_tts_voices.py`用) | — |
| `PETIT_CHARACTER_ID` / `PETIT_SESSION_USER` | `record_session.py`用 | `petit` / — |
| `PROJECT_DIR` | `start_chat_session.sh`がClaude Codeのセッション保存先を特定するのに使う | カレントディレクトリ |
