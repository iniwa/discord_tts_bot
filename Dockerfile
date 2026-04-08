FROM python:3.11-slim

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    open-jtalk \
    open-jtalk-mecab-naist-jdic \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 【重要】音声ファイル用のディレクトリ作成とコピー
# コード内の VOICE_PATH = "/voice/mei_normal.htsvoice" に合わせる
RUN mkdir -p /voice
COPY mei_normal.htsvoice /voice/mei_normal.htsvoice

# 非rootユーザーの作成
RUN useradd -r -s /bin/false appuser

# ソースコードと辞書をコピー
COPY . .

# エントリポイント: tmpfs・マウントファイルの権限修正後にappuserで実行
CMD ["sh", "-c", "chown appuser:appuser /ram_cache /app/word_dict.json /app/settings.json 2>/dev/null; exec su -s /bin/sh appuser -c 'python bot.py'"]