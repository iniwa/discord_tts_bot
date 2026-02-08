FROM python:3.11-slim

# 必要なパッケージのインストール
# open-jtalk, open-jtalk-mecab-naist-jdic, ffmpeg
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

# ソースコードのコピー
COPY . .

# 実行
CMD ["python", "bot.py"]