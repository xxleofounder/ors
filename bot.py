from telethon import Button
from telethon import TelegramClient, events
from asyncio import sleep
from Config import Config
import asyncio
import subprocess
from telethon import events
import yt_dlp
import os
from telethon import events, errors
import logging
import re 
import lyricsgenius
import random
from telethon import Button, events

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = Config.API_ID
api_hash = Config.API_HASH
bot_token = Config.BOT_TOKEN

# Sudo/owner ID'yi buraya gir
OWNER_ID = 8276543841

client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

GENIUS_TOKEN = "IEr1zibeW1gnG5yS0JTRqUFzo6iiL8-fOhQXWMGOhUK74zbKYfYwm8XmcO52oGL3"

# ʀᴀsᴛɢᴇʟᴇ ᴛᴜ̈ʀ
keywords = {
    "Rap": ["rap", "hiphop", "trap", "rap Türkçe"],
    "Pop": ["pop", "slow", "pop Türkçe", "aşk"],
    "Arabesk": ["arabesk", "türk arabesk", "arabesk slow"],
    "Diger": ["türkü", "rock", "jazz", "klasik"]
}
  

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    user = await event.get_sender()
    first_name = user.first_name
    user_id = user.id
    username = user.username if user.username else "Kullanıcı adı yok"

    # Kullanıcıya hoş geldin mesajı
    await client.send_file(
        event.chat_id,
        "https://r.resimlink.com/wk3gFJ.jpg",
        caption=(
            f"👋🏻 ᴍᴇʀʜᴀʙᴀ {first_name}, ᴀʀᴛᴢ ᴍᴜsɪᴄ\n\n"
            "🎧 Bᴇɴ YᴏᴜTᴜʙᴇ iʟᴇ iʟɢiʟi ᴄ̧ᴇşɪᴛʟɪ ᴀʀᴀᴍᴀʟᴀʀ ʏᴀᴘᴀʀ, ᴀʀᴀᴅɪɢ̆ɪɴɪᴢ ᴍᴜ̈ᴢɪğɪ ʙᴜʟᴜᴘ sɪᴢᴇ ᴍᴘ3 ᴏʟᴀʀᴀᴋ ɢᴏ̈ɴᴅᴇʀɪʀɪᴍ.\n\n"
            "📣 ᴋᴜʟʟᴀɴɪᴍ ᴋᴏɴᴜsᴜɴᴅᴀ ʏᴀʀᴅɪᴍ ɪçɪɴ ʜᴇʟᴘ ʙᴜᴛᴏɴᴜɴᴜ ᴋᴜʟʟᴀɴᴀʙɪʟɪʀsɪɴɪᴢ."
        ),
        buttons=[
            [Button.url("🥇 ᴏᴡɴᴇʀ", "https://t.me/artzfounder")],
            [Button.inline("ℹ️ ʜᴇʟᴘ", data="help")]
        ],
        link_preview=False
    )

    # Owner'a bildirim gönder
    await client.send_message(
        OWNER_ID,
        f"👤 kullanıcı /start kullandı:\n\n"
        f"• İsim: {first_name}\n"
        f"• ID: {user_id}\n"
        f"• Kullanıcı Adı: @{username}"
    )


# Inline Help Menüsü
@client.on(events.CallbackQuery(data="help"))
async def help_menu(event):
    await event.edit(
        "📚 ᴋᴏᴍᴜᴛʟᴀʀɪᴍ ᴀşᴀɢ̆ɪᴅᴀ ʏᴇʀ ᴀʟɪʏᴏʀ:\n\n"
        "➪ `/ara` - ʏᴏᴛᴜʙᴇᴅᴇ ᴍᴜsɪc, ᴠᴇʏᴀ ᴅᴏsʏᴀ sᴇsɪ ɪɴᴅɪʀɪʀ\n\n"
        "➪ `/song` - ᴀʀᴀᴅɪɢ̆ɪɴɪᴢ ᴘᴀʀᴄ̧ᴀɴɪɴ sᴏ̈ᴢʟᴇʀɪɴɪ ʙᴜʟᴜᴘ sɪᴢᴇ iʟᴇᴛiʀ\n\n"
        "➪ `/random` - siᴢᴇ ʀᴀsᴛɢᴇʟᴇ ʏᴏᴜᴛᴜʙᴇ'ᴅᴇ ᴘᴀʀᴄ̧ᴀ ʙᴜʟᴜᴘ ᴀᴛᴀʀ\n\n"
        "➪ `/yenile` - sᴜɴᴜᴄᴜ'ʏᴜ ʏᴇɴɪᴅᴇɴ ʙᴀşʟᴀᴛɪʀ, ʜᴀᴛᴀʟᴀʀɪ ɢɪᴅᴇʀɪʀ",
        buttons=[[Button.inline("⬅️ ɢᴇʀɪ ᴅᴏ̈ɴ", data="starta")]],
        link_preview=False
    )


# Inline Start’a Geri Dön
@client.on(events.CallbackQuery(data="starta"))
async def starta(event):
    user = await event.get_sender()
    first_name = user.first_name

    await event.edit(
        f"👋🏻 ᴍᴇʀʜᴀʙᴀ {first_name}, ᴀʀᴛᴢ ᴍᴜsɪᴄ\n\n"
        "🎧 Bᴇɴ YᴏᴜTᴜʙᴇ iʟᴇ iʟɢiʟi ᴄ̧ᴇşɪᴛʟɪ ᴀʀᴀᴍᴀʟᴀʀ ʏᴀᴘᴀʀ, ᴀʀᴀᴅɪɢ̆ɪɴɪᴢ ᴍᴜ̈ᴢɪğɪ ʙᴜʟᴜᴘ sɪᴢᴇ ᴍᴘ3 ᴏʟᴀʀᴀᴋ ɢᴏ̈ɴᴅᴇʀɪʀɪᴍ.\n\n"
        "📣 ᴋᴜʟʟᴀɴɪᴍ ᴋᴏɴᴜsᴜɴᴅᴀ ʏᴀʀᴅɪᴍ ɪçɪɴ ʜᴇʟᴘ ʙᴜᴛᴏɴᴜɴᴜ ᴋᴜʟʟᴀɴᴀʙɪʟɪʀsɪɴɪᴢ.",
        buttons=[
            [Button.url("🥇 ᴏᴡɴᴇʀ", "https://t.me/artzfounder")],
            [Button.inline("ℹ️ ʜᴇʟᴘ", data="help")]
        ],
        link_preview=False
    )


@client.on(events.NewMessage(pattern=r"^/ara (.+)"))
async def ara(event):
    query = event.pattern_match.group(1)
    status = await event.reply("🎵 ᴍᴜ̈ᴢiɢ̆i ʏᴏᴜᴛᴜʙᴇ'ᴅᴇ ᴀʀɪʏᴏʀᴜᴍ...")

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    filename = None  # dosyayi sunucuda bırakma sil

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            if not info or "entries" not in info or len(info["entries"]) == 0:
                await status.edit("❌ ᴜ̈ᴢɢᴜ̈ɴᴜ̈ᴍ ʙᴜ sᴇs ᴅᴏsʏᴀsɪɴɪ, ʏᴏᴜᴛᴜʙᴇᴅᴇ ʙᴜʟᴀᴍᴀᴅɪᴍ.")
                return

            video = info["entries"][0]
            title = video.get("title", "Bilinmeyen Başlık")
            safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
            filename = f"{safe_title}.mp3"

        await status.edit("✅ ᴘᴀʀᴄ̧ᴀʏɪ ʙᴜʟᴅᴜᴍ")
        await status.edit("📤 ᴘᴀʀᴄ̧ᴀʏɪ ɢᴏ̈ɴᴅᴇʀɪʏᴏʀᴜᴍ, ʙɪʀ sᴀɴɪʏᴇ...")

        await event.reply(file=filename, message=f"🎶 {title}")

    except Exception as e:
        await event.reply(f"❌ ʜᴀᴛᴀ ᴏʟᴜşᴛᴜ: {e}")

    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)
        await status.delete()


@client.on(events.NewMessage(pattern="^/yenile$"))
async def yenile(event):
    # Başlangıç mesajı
    mesaj = await event.respond("🔄 ʏᴇɴɪᴅᴇɴ ʙᴀşʟᴀᴛɪʟɪʏᴏʀ: %0")

    for yuzde in range(10, 101, 10):
        await asyncio.sleep(0.5)
        await mesaj.edit(f"🔄 ʏᴇɴɪᴅᴇɴ ʙᴀşʟᴀᴛɪʟɪʏᴏʀ: %{yuzde}")

  
    try:
        ping_output = subprocess.check_output(
            ["ping", "-c", "1", "8.8.8.8"], universal_newlines=True
        )
        # Çıktıdan süreyi al
        ping_line = [line for line in ping_output.split("\n") if "time=" in line][0]
        ping_ms = ping_line.split("time=")[1].split(" ")[0]
    except Exception:
        ping_ms = "ᴜ̈ᴢɢᴜ̈ɴᴜ̈ᴍ, ᴘɪɴɢ ᴏ̈ʟᴄ̧ᴜ̈ʟᴍᴇᴅɪ"

    await asyncio.sleep(2)
    await mesaj.edit(f"✅ ʏᴇɴɪʟᴇᴍᴇ ʙɪᴛᴛɪ!! ᴘɪɴɢ: {ping_ms} ms\nʙᴏᴛ ᴀʀᴛɪᴋ ᴅᴀʜᴀ sᴛᴀʙɪʟ, ɪʏɪ sᴏʜʙᴇᴛʟᴇʀ..")


genius = lyricsgenius.Genius(GENIUS_TOKEN, timeout=15, skip_non_songs=True)

@client.on(events.NewMessage(pattern=r"^/song (.+)"))
async def song(event):
    query = event.pattern_match.group(1)
    status = await event.reply(f"🔎 '{query}' şᴀʀᴋɪsɪɴɪɴ sᴏ̈ᴢʟᴇʀɪɴɪ ᴀʀɪʏᴏʀᴜᴍ...")

    try:
        song = genius.search_song(query)
        if song and song.lyrics:
            lyrics = song.lyrics
            if len(lyrics) > 4000: 
                lyrics = lyrics[:4000] + "\n\n[...Daha fazla söz var]"
            await event.reply(f"🎶 {song.title} - {song.artist}\n\n{lyrics}")
        else:
            await event.reply("❌ ᴜ̈ᴢɢᴜ̈ɴᴜ̈ᴍ, şᴀʀᴋɪ sᴏ̈ᴢʟᴇʀɪɴɪ ʙᴜʟᴀᴍᴀᴅɪᴍ")
    except Exception as e:
        await event.reply(f"❌ ʙɪʀ ʜᴀᴛᴀ ᴏʟᴜşᴛᴜ: {e}")
    finally:
        await status.delete()


@client.on(events.NewMessage(pattern="^/random$"))
async def random_genre(event):
    buttons = [
        [Button.inline("🎤 ʀᴀᴘ", "Rap"), Button.inline("🎵 ᴘᴏᴘ", "Pop")],
        [Button.inline("🎻 ᴀʀᴀʙᴇsᴋ", "Arabesk"), Button.inline("🎶 ᴅiɢ̆ᴇʀ", "Diger")]
    ]
    await event.respond("🎲 **ᴀʀᴀɴᴀᴄᴀᴋ şᴀʀᴋɪ ᴛᴜ̈ʀᴜ̈ɴᴜ̈ sᴇᴄ̧!:**", buttons=buttons, parse_mode="md")


@client.on(events.CallbackQuery)
async def callback_random(event):
    choice = event.data.decode("utf-8")  # seçilen tür
    if choice not in keywords:
        await event.answer("❌ ʜᴀᴛᴀ: ʙɪʟɪɴᴍᴇʏᴇɴ ᴛᴜ̈ʀ")
        return

    await event.answer(f"🔎 {choice} ᴛᴜ̈ʀᴜ̈ɴᴅᴇ şᴀʀᴋɪ sᴇᴄ̧ɪʟɪʏᴏʀ...")
    query = random.choice(keywords[choice])
    status = await event.edit(f"⏳ '{query}' ᴛᴜ̈ʀᴜ̈ɴᴅᴇ ʀᴀsᴛɢᴇʟᴇ şᴀʀᴋɪ ᴀʀᴀɴɪʏᴏʀ...")

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if not info or "entries" not in info or len(info["entries"]) == 0:
                await status.edit("❌ ᴏʜʜ, şᴀʀᴋɪʏɪ ʙᴜʟᴍᴀᴅɪᴍ")
                return

            video = info["entries"][0]
            title = video.get("title", "Bilinmeyen Şarkı")
            url = video.get("webpage_url")

            await status.edit(f"🎶 **ʀᴀɴᴅᴏᴍ şᴀʀᴋɪ:**\n➡️ [{title}]({url})", parse_mode="md")

    except Exception as e:
        await status.edit(f"❌ ʜᴀᴛᴀ ᴏʟᴜşᴛᴜ: {e}")  


print(">> 🛠️ Artz , Başarıyla Aktifleştirildi...<<")
client.run_until_disconnected()
