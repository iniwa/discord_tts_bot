# **🎵 Simple Discord TTS Bot for Raspberry Pi**

Raspberry Pi（Docker）での運用を想定した、シンプルで軽量なDiscord読み上げBotです。

Open JTalkを使用しており、外部APIを使用せずにローカルで音声合成を行います。

ビルド済みのDockerイメージを公開しているため、Raspberry Pi等のDocker環境があればすぐに利用可能です。

🤖 **Note:** 本プロジェクトのソースコードはAIの支援を受けて作成されています。

## **✨ 特徴**

* **🍓 Raspberry Pi 最適化:** Raspberry Pi 4でのセルフホストを前提に設計されています。  
* **🚀 軽量・シンプル:** 読み上げに必要な最小限の機能に絞っています。  
* **⚡ SDカードに優しい:** 音声生成や辞書データ展開にRAMディスク（tmpfs）を使用する設計になっており、SDカードへの書き込み負荷を軽減し、レスポンスを高速化しています。  
* **🐳 Docker完全対応:** Docker Hub (GHCR) からイメージをプルするだけで起動できます。

## **📦 必要要件**

* **ハードウェア:** Raspberry Pi 4 (またはその他Dockerが動くLinuxマシン)  
* **ソフトウェア:** Docker, Docker Compose (または Portainer)  
* **Discord Bot Token:** 開発者ポータルで取得したもの

## **🚀 クイックスタート (推奨)**

すでにビルドされたDockerイメージを使用する方法です。PortainerのStacks機能、または docker-compose で簡単に起動できます。

### **1\. docker-compose.yaml の作成**

任意のディレクトリに docker-compose.yaml を作成し、以下の内容を記述します。

（Portainerを使用している場合は、"Stacks" \> "Add stack" のWebエディタに貼り付けてください）

services:  
  discord-bot:  
    image: ghcr.io/iniwa/discord\_tts\_bot:latest  
    container\_name: discord\_tts\_bot  
    restart: always  
    \# パフォーマンス最適化（RAMディスク活用）  
    tmpfs:  
      \- /ram\_cache  
    environment:  
      \# 自身のBotトークンに書き換えてください  
      \- DISCORD\_TOKEN=your\_token\_here  
    \# 辞書データを永続化したい（再起動しても登録単語を残したい）場合は  
    \# 手元に word\_dict.json を用意してコメントアウトを外してください  
    \# volumes:  
    \#   \- ./word\_dict.json:/app/word\_dict.json

### **2\. コンテナの起動**

**Docker Composeの場合:**

docker-compose up \-d

**Portainerの場合:**

"Deploy the stack" ボタンを押してデプロイします。

## **🛠️ 開発者向けセットアップ (ソースからビルド)**

カスタマイズを行いたい場合は、リポジトリをクローンしてビルドしてください。

1. リポジトリをクローン  
2. mei\_normal.htsvoice (音響モデル) を配置  
3. ビルドして起動:  
   docker-compose up \-d \--build

## **🎮 使い方 (コマンド)**

このBotはスラッシュコマンドに対応しています。

| コマンド | 説明 |
| :---- | :---- |
| /join | ボイスチャンネルに接続し、読み上げを開始します。 |
| /leave | ボイスチャンネルから切断します。 |
| /dict-add \[word\] \[read\] | 辞書に単語登録します（例: /dict-add w わら）。 |
| /dict-del \[word\] | 辞書から単語を削除します。 |
| /dict-list | 登録されている単語一覧を表示します。 |
| /help | 利用可能なコマンド一覧を表示します。 |

## **⚙️ 技術的な詳細**

* **RAMキャッシュ:** コンテナ内の /ram\_cache をtmpfs（メモリ）としてマウントしています。Bot起動時にOpen JTalkの辞書と音声データをここに展開し、音声生成処理をすべてメモリ上で行うことで高速化を実現しています。  
* **辞書機能:** デフォルトの辞書データは word\_dict.json です。

## **⚠️ 免責事項**

* 本ツールの使用によって生じた不利益について、作者は一切の責任を負いません。  
* AIによって生成されたコードが含まれるため、予期しない挙動をする可能性があります。

## **©️ ライセンス・クレジット**

本プロジェクトのソースコードは **MIT License** のもとで公開されています。

また、本ソフトウェアの音声合成には、名古屋工業大学大学院工学研究科によって開発された **HTS Voice "Mei"** を使用しています。

**HTS Voice "Mei"**
* **Copyright:** Copyright (c) 2009-2018 Nagoya Institute of Technology Department of Computer Science
* **License:** [Creative Commons Attribution 3.0](http://creativecommons.org/licenses/by/3.0/)
* **Official Site:** [MMDAgent](http://www.mmdagent.jp/)