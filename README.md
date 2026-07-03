# m5-petit-scripts

## [EnglishPage](./README_en.md)

M5 Petit用の汎用ユーティリティスクリプト集です。ファームウェア(.ino)もここに置きます(準備中)。

いずれのスクリプトも`$PETIT_DATA_DIR`(デフォルト`~/petit_data`)配下のデータを扱い、[m5-petit-app](https://github.com/PetitOnes/m5-petit-app)と同じディレクトリ構成(`characters/<character_id>/chat_histories/`、`characters/<character_id>/stream_logs/`など)を読み書きします。

## スクリプト一覧

### メールボックス

- `mark_mail_read.py <character_id> <filename...>` / `--all` — メールを既読にする
- `list_unread_mail.py <character_id>` — 未読メール一覧を表示

### チャットログ・記録

m5-petit-appのHTTP API経由ではなく、ターミナル等から直接Claudeを呼ぶ場合にログを共有するためのスクリプトです。

- `append_chat_log.py --character-id <id> --role <role> --text <text>` — 会話ログ(「会話」タブ用)に1件追記
- `save_chat_stream_log.py` — stream-json形式のログ(「記録」タブ用)を保存。JSON入力(stdinまたはファイル引数)
- `read_stream.py <file or character_id>` — stream-jsonログを色付きで読みやすく表示
- `format_stream_log.py [file]` — stream-jsonをパイプで受けてプレーンテキストログに変換

### コスト集計

- `generate_cost_summary.py [--budget USD] [--reset-day N]` — `characters/*/stream_logs/`からコストを集計し、Markdownサマリーを書き出す

### 音声

- `register_tts_voices.py --chars <id...> --tts-url <url> --asr-url <url>` — キャラのTTS音声を生成して話者認識(ASR)に登録

## 環境変数

| 変数名 | 説明 | デフォルト |
| --- | --- | --- |
| `PETIT_DATA_DIR` | データディレクトリ(m5-petit-appと共有) | `~/petit_data` |
| `TTS_URL` / `ASR_URL` | TTS/ASRサーバーのURL(`register_tts_voices.py`用) | — |
