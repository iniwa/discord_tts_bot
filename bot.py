import discord
from discord import app_commands
from discord.ext import commands
import os
import subprocess
import uuid
import json
import asyncio
import re
import romkan
from collections import defaultdict
import shutil

# --- 変更: RAMディスク設定とデータ展開 ---
# Docker Composeで割り当てたtmpfsのパス
RAM_ROOT = "/ram_cache"

# 元のファイルパス（ディスク上）
ORIGINAL_DIC_PATH = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
ORIGINAL_VOICE_PATH = "/voice/mei_normal.htsvoice"

# RAM上の配置パス
DIC_PATH = os.path.join(RAM_ROOT, "dic")
VOICE_PATH = os.path.join(RAM_ROOT, "voice.htsvoice")
TEMP_DIR = RAM_ROOT  # 一時ファイルもRAM上に保存

print("Copying assets to RAM...")
# 辞書ディレクトリをRAMへコピー
if not os.path.exists(DIC_PATH):
    shutil.copytree(ORIGINAL_DIC_PATH, DIC_PATH)

# 音声ファイルをRAMへコピー
if not os.path.exists(VOICE_PATH):
    shutil.copy(ORIGINAL_VOICE_PATH, VOICE_PATH)
print("Assets copied to RAM.")

# open_jtalkのウォームアップ（初回遅延を回避）
_warmup_path = os.path.join(RAM_ROOT, "_warmup.wav")
subprocess.run(
    ["open_jtalk", "-x", DIC_PATH, "-m", VOICE_PATH, "-ow", _warmup_path],
    input="テスト".encode("utf-8"),
    stderr=subprocess.DEVNULL,
)
if os.path.exists(_warmup_path):
    os.remove(_warmup_path)
print("Open JTalk warmed up.")

# インテントの設定
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

# --- BOTクラスの定義 ---
class TTSBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=intents, help_command=None)
        # 読み上げ対象のチャンネルID管理: {guild_id: channel_id}
        self.active_channels = {}
        # 読み上げキュー管理: {guild_id: [filename1, filename2, ...]}
        self.queues = defaultdict(list)
        # 再生状態管理: {guild_id: True/False}
        self.playing_status = defaultdict(bool)

    async def setup_hook(self):
        await self.tree.sync()

bot = TTSBot()

# Open JTalkの設定
OPEN_JTALK_BIN = "open_jtalk"
DICT_FILE = "word_dict.json"

# 設定：省略する文字数
MAX_LENGTH = 50

# --- 辞書関連 ---

def load_dict():
    if os.path.exists(DICT_FILE):
        with open(DICT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_dict(data):
    with open(DICT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

word_dict = load_dict()

# --- 共通関数 ---

async def cleanup_and_disconnect(guild):
    """
    切断時の後片付けと切断処理を行う共通関数
    """
    # キューのクリア
    if guild.id in bot.queues:
        bot.queues[guild.id].clear()
    
    # 管理用変数のリセット
    bot.active_channels.pop(guild.id, None)
    bot.playing_status[guild.id] = False

    # 切断
    if guild.voice_client:
        await guild.voice_client.disconnect()

# --- 音声生成関数 ---

def generate_voice(text, output_path):
    cmd = [
        OPEN_JTALK_BIN,
        "-x", DIC_PATH,
        "-m", VOICE_PATH,
        "-ow", output_path,
        "-r", "1.0",
        "-jf", "1.0",
    ]
    try:
        subprocess.run(cmd, input=text.encode("utf-8"), check=True, stderr=subprocess.PIPE)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            return True
        return False
    except Exception as e:
        print(f"[Error] generate_voice: {e}")
        return False

# --- 再生管理関数 ---

def play_next(guild):
    # キューが空なら再生終了
    if not bot.queues[guild.id]:
        bot.playing_status[guild.id] = False
        return

    bot.playing_status[guild.id] = True
    audio_path = bot.queues[guild.id].pop(0)

    voice_client = guild.voice_client
    if not voice_client or not voice_client.is_connected():
        bot.playing_status[guild.id] = False
        if os.path.exists(audio_path):
            os.remove(audio_path)
        return

    try:
        source = discord.FFmpegPCMAudio(audio_path)
        
        def after_playing(error):
            if os.path.exists(audio_path):
                os.remove(audio_path)
            play_next(guild)

        voice_client.play(source, after=after_playing)
    
    except Exception:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        play_next(guild)

# --- コマンド群 ---

@bot.tree.command(name="join", description="ボイスチャンネルに参加します")
async def join_channel(interaction: discord.Interaction):
    await interaction.response.defer()
    
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        await channel.connect()
        bot.active_channels[interaction.guild.id] = interaction.channel.id
        await interaction.followup.send(f"🔊 **{channel.name}** に参加しました。")
    else:
        await interaction.followup.send("ボイスチャンネルに参加してから実行してください。", ephemeral=True)

@bot.tree.command(name="bye", description="ボイスチャンネルから退出します")
async def bye(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await cleanup_and_disconnect(interaction.guild)
        await interaction.response.send_message("ばいばい")
    else:
        await interaction.response.send_message("今は通話に参加してないよ。", ephemeral=True)

@bot.tree.command(name="add", description="辞書に単語を登録します")
@app_commands.describe(word="登録する単語", reading="読み方")
async def add(interaction: discord.Interaction, word: str, reading: str):
    word_dict[word] = reading
    save_dict(word_dict)
    await interaction.response.send_message(f'📝 登録: **{word}** → {reading}')

@bot.tree.command(name="remove", description="辞書から単語を削除します")
@app_commands.describe(word="削除する単語")
async def remove(interaction: discord.Interaction, word: str):
    if word in word_dict:
        del word_dict[word]
        save_dict(word_dict)
        await interaction.response.send_message(f'🗑️ 削除: {word}')
    else:
        await interaction.response.send_message(f'未登録です: {word}', ephemeral=True)

@bot.tree.command(name="list", description="登録単語一覧を表示")
async def list_dict(interaction: discord.Interaction):
    if not word_dict:
        await interaction.response.send_message("辞書は空です。", ephemeral=True)
        return
    items = [f"**{k}**: {v}" for k, v in word_dict.items()]
    message = "📖 **辞書一覧**\n" + "\n".join(items)
    if len(message) > 2000:
        message = message[:1990] + "..."
    await interaction.response.send_message(message, ephemeral=True)

@bot.tree.command(name="help", description="コマンド一覧を表示します")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(title="コマンド一覧", color=discord.Color.blue())
    embed.add_field(name="/join", value="ボイスチャンネルに参加し、読み上げを開始します。", inline=False)
    embed.add_field(name="/bye", value="ボイスチャンネルから退出します。", inline=False)
    embed.add_field(name="/add `word` `reading`", value="辞書に単語と読み方を登録します。", inline=False)
    embed.add_field(name="/remove `word`", value="辞書から単語を削除します。", inline=False)
    embed.add_field(name="/list", value="登録されている単語の一覧を表示します。", inline=False)
    embed.add_field(name="/help", value="このヘルプを表示します。", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# --- イベント ---

@bot.event
async def on_voice_state_update(member, before, after):
    """
    ボイスチャンネルの状態が変わったときに呼ばれる
    """
    voice_client = member.guild.voice_client
    if not voice_client or not voice_client.is_connected():
        return

    # メンバーが退出、または移動したチャンネルが、BOTのいるチャンネルだった場合
    if before.channel and before.channel.id == voice_client.channel.id:
        # BOT以外に誰もいなくなったら切断
        if len(voice_client.channel.members) == 1:
            await cleanup_and_disconnect(member.guild)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    target_channel_id = bot.active_channels.get(message.guild.id)
    if message.channel.id != target_channel_id:
        return

    if not message.guild.voice_client or not message.guild.voice_client.is_connected():
        return

    text = message.content
    # --- 修正: 改行を読点に置換 ---
    text = text.replace('\n', '、')
    # ---------------------------
    text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', 'ユーアールエル', text)

    # --- 修正ここから ---
    # 辞書適用：文字数が長い順にソートして適用（iniwa等の長い単語を先に変換するため）
    sorted_items = sorted(word_dict.items(), key=lambda x: len(x[0]), reverse=True)

    for word, reading in sorted_items:
        # 'w' や 'ww' の場合、前後に英数字がある場合は置換しない（BMW対策）
        if re.fullmatch(r'w+', word, re.IGNORECASE):
            pattern = r'(?<![a-zA-Z0-9])' + re.escape(word) + r'(?![a-zA-Z0-9])'
            text = re.sub(pattern, reading, text)
        else:
            text = text.replace(word, reading)
    # --- 修正ここまで ---

    text = re.sub(r'<:(\w+):\d+>', r'\1', text)
    text = romkan.to_hiragana(text)

    if len(text) > MAX_LENGTH:
        text = text[:MAX_LENGTH] + "、以下省略"

    if not text.strip():
        return

    filename = os.path.join(TEMP_DIR, f"output_{uuid.uuid4()}.wav")
    loop = asyncio.get_running_loop()
    success = await loop.run_in_executor(None, generate_voice, text, filename)

    if success:
        bot.queues[message.guild.id].append(filename)
        if not bot.playing_status[message.guild.id]:
            play_next(message.guild)

token = os.getenv("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("Error: DISCORD_TOKEN is not set.")