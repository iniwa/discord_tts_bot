# Simple Discord TTS Bot

Raspberry Pi (Docker) での運用を想定した、シンプルで軽量な Discord 読み上げ Bot です。

Open JTalk を使用し、外部 API なしでローカル音声合成を行います。

## 特徴

- **Raspberry Pi 最適化** - ARM64 (Raspberry Pi 4) でのセルフホストを前提に設計
- **軽量・シンプル** - 読み上げに必要な最小限の機能に絞った構成
- **RAMキャッシュ** - tmpfs を活用し、辞書・音声データをメモリ上で処理。SDカードへの書き込みを軽減
- **Docker 対応** - GHCR からイメージをプルするだけで起動可能

## 必要要件

- Docker / Docker Compose (または Portainer)
- Discord Bot Token ([Developer Portal](https://discord.com/developers/applications) で取得)

## セットアップ

### 1. docker-compose.yaml を作成

```yaml
services:
  discord-bot:
    image: ghcr.io/<your-username>/discord_tts_bot:latest
    container_name: discord_tts_bot
    tmpfs:
      - /ram_cache
    volumes:
      # 辞書ファイルの永続化（ホスト側パスは環境に合わせて変更）
      - /path/to/word_dict.json:/app/word_dict.json
    environment:
      - DISCORD_TOKEN=<your-token>
      - TZ=Asia/Tokyo
    restart: unless-stopped
```

### 2. 辞書ファイルの準備

ホスト側に `word_dict.json` を作成します。空の辞書で始める場合:

```json
{}
```

サンプル:

```json
{
    "w": "わら",
    "ww": "わらわら",
    "discord": "でぃすこーど"
}
```

### 3. 起動

```bash
docker compose up -d
```

Portainer の場合は Stacks > Add stack から yaml を貼り付けてデプロイしてください。

## コマンド一覧

| コマンド | 説明 |
| --- | --- |
| `/join` | ボイスチャンネルに参加し、読み上げを開始 |
| `/bye` | ボイスチャンネルから退出 |
| `/add <word> <reading>` | 辞書に単語を登録 (例: `/add w わら`) |
| `/remove <word>` | 辞書から単語を削除 |
| `/list` | 登録単語の一覧を表示 |
| `/notify` | VC参加通知の読み上げを ON/OFF |
| `/help` | コマンド一覧を表示 |

## 読み上げの仕様

- `/join` を実行したテキストチャンネルのメッセージを読み上げます
- 同じVCに接続中に別のテキストチャンネルで `/join` すると、読み上げ対象が切り替わります
- URL は「ユーアールエル」に変換されます
- カスタム絵文字は絵文字名のみ読み上げます
- 辞書は文字数の長い単語から優先的に適用されます
- 50文字を超えるメッセージは省略されます
- BOT のいるVCから全員退出すると自動で切断します
- `/notify` を ON にすると、VCにユーザーが参加した際に「○○さんが参加しました」と読み上げます

## 開発者向け (ソースからビルド)

```bash
git clone <repository-url>
cd discord_tts_bot
# mei_normal.htsvoice をプロジェクトルートに配置
docker compose up -d --build
```

### 技術スタック

- Python 3.11 / discord.py
- Open JTalk (音声合成) + MeCab辞書 (形態素解析)
- FFmpeg (音声再生)
- romkan (ローマ字→ひらがな変換)

## ライセンス

本プロジェクトのソースコードは **MIT License** のもとで公開されています。

本ソフトウェアは以下のサードパーティソフトウェア・データを使用しています。
詳細は [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES) を参照してください。

- **Open JTalk** (Modified BSD License) - Copyright (c) 2008-2018 Nagoya Institute of Technology
- **HTS Voice "Mei"** ([CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)) - Copyright (c) 2009-2015 Nagoya Institute of Technology / [MMDAgent](http://www.mmdagent.jp/)
