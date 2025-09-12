import asyncio
import os
from pyrogram import Client, filters
import yt_dlp

# -----------------------------
# Kullanıcı bilgileri
# -----------------------------
api_id = 21883581
api_hash = "c3b4ba58d5dada9bc8ce6c66e09f3f12"
bot_token = "8449988873:AAFAAdg4cwLjE2GtiBk891OfE85o-xRQVuc"
user_session = "BAFN6r0As-zf7RjX9rV9mx-FpqRb6m1mIzW8GBFZ-0lH-rfOsyjUOLjF6AcExzhOdeaDf1CGh8ljBH2j169S3ujwrKYFSztRBg4dS2kfjJWU25M2sPC9Jk_P5l-ybuoKDYGjdt7tEVpqlrhMlCmIZ4-YNVqESuM8DeKaLXh4_PmRz0SrBWdsBkCfYnG4IogFu49e4Ej-bEZ8rQBPpvDicnIpd8JjUl6t98BDPO0mqlBUsWY54wuI534tJKln8iJvDa-HsDuHuUmOgN37EtWgI4YP5HQX1MYWQZCa1c_URR-rOKgHJJBLIsYZEL2NCoQnVTzNkH-vShLXeys3X2Aoc2ZbEpvjmAAAAAHnAcMFAA"

# -----------------------------
# Başlatma
# -----------------------------
bot = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
user = Client("user_session", api_id=api_id, api_hash=api_hash, session_string=user_session)

# -----------------------------
# Global değişken
# -----------------------------
is_playing = False
current_task = None

# -----------------------------
# Şarkı çalma fonksiyonu (ffmpeg yok)
# -----------------------------
async def play_music(query):
    global is_playing
    is_playing = True
    filename = "song.mp3"

    if not query.startswith("http"):
        query = f"ytsearch1:{query}"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            if "entries" in info:
                info = info["entries"][0]
            title = info.get("title", "Bilinmeyen Şarkı")
            duration = info.get("duration", 0)
    except Exception as e:
        is_playing = False
        return None, str(e)

    # Simülasyon: şarkı çalınıyormuş gibi bekle
    try:
        await asyncio.sleep(min(duration, 300))  # maksimum 5 dakika
    except asyncio.CancelledError:
        is_playing = False
        if os.path.exists(filename):
            os.remove(filename)
        return title, "Çalma iptal edildi"

    # Dosyayı sil
    if os.path.exists(filename):
        os.remove(filename)

    is_playing = False
    return title, None

# -----------------------------
# /start komutu
# -----------------------------
@bot.on_message(filters.command("start"))
async def start(_, msg):
    if msg.chat.type == "private":
        await msg.reply(
            "👋 Merhaba!\n\n"
            "Ben bir 🎶 Müzik Çalma Botuyum.\n"
            "Komutlar:\n"
            "• /cal <şarkı ismi veya link> → Müzik çal\n"
            "• /dur → Çalmayı durdur\n"
            "• /pause → Duraklat (simülasyon)\n"
            "• /resume → Devam ettir (simülasyon)\n\n"
            "ℹ️ Beni gruplara ekleyip oradan da kullanabilirsin."
        )
    else:
        await msg.reply("🎶 Bot aktif! Komutlar: /cal /dur /pause /resume")

# -----------------------------
# /cal komutu
# -----------------------------
@bot.on_message(filters.command("cal"))
async def cal(_, msg):
    global current_task, is_playing
    if len(msg.command) < 2:
        await msg.reply("❌ Lütfen şarkı ismi veya link gir: /cal <şarkı>")
        return

    if is_playing:
        await msg.reply("❌ Zaten bir şarkı çalınıyor. /dur ile durdurabilirsin.")
        return

    query = " ".join(msg.command[1:])
    await msg.reply(f"🔎 '{query}' aranıyor ve çalınıyor...")

    current_task = asyncio.create_task(play_music(query))
    title, error = await current_task

    if error:
        await msg.reply(f"❌ Çalma hatası: {error}")
    else:
        await msg.reply(f"▶️ Çalınıyor: {title}\n✅ Şarkı çalındıktan sonra silindi.")

# -----------------------------
# /dur komutu
# -----------------------------
@bot.on_message(filters.command("dur"))
async def dur(_, msg):
    global current_task, is_playing
    if current_task and not current_task.done():
        current_task.cancel()
        is_playing = False
        await msg.reply("🛑 Çalma durduruldu")
    else:
        await msg.reply("❌ Çalan bir şarkı yok")

# -----------------------------
# /pause komutu (simülasyon)
# -----------------------------
@bot.on_message(filters.command("pause"))
async def pause(_, msg):
    await msg.reply("⏸ Duraklat (simülasyon, ffmpeg yok)")

# -----------------------------
# /resume komutu (simülasyon)
# -----------------------------
@bot.on_message(filters.command("resume"))
async def resume(_, msg):
    await msg.reply("▶️ Devam et (simülasyon, ffmpeg yok)")

# -----------------------------
# Başlat
# -----------------------------
async def main():
    await bot.start()
    await user.start()
    print("✅ Bot ve Userbot çalışıyor ve aktif!")
    await asyncio.get_event_loop().create_future()

asyncio.run(main())
