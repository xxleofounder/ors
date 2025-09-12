import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
import yt_dlp

# 🔹 Kullanıcı bilgilerini buraya gir
api_id = 21883581         # Telegram API ID
api_hash = "c3b4ba58d5dada9bc8ce6c66e09f3f12"  # Telegram API HASH
bot_token = "8449988873:AAFAAdg4cwLjE2GtiBk891OfE85o-xRQVuc"  # Bot token
user_session = "BAFN6r0As-zf7RjX9rV9mx-FpqRb6m1mIzW8GBFZ-0lH-rfOsyjUOLjF6AcExzhOdeaDf1CGh8ljBH2j169S3ujwrKYFSztRBg4dS2kfjJWU25M2sPC9Jk_P5l-ybuoKDYGjdt7tEVpqlrhMlCmIZ4-YNVqESuM8DeKaLXh4_PmRz0SrBWdsBkCfYnG4IogFu49e4Ej-bEZ8rQBPpvDicnIpd8JjUl6t98BDPO0mqlBUsWY54wuI534tJKln8iJvDa-HsDuHuUmOgN37EtWgI4YP5HQX1MYWQZCa1c_URR-rOKgHJJBLIsYZEL2NCoQnVTzNkH-vShLXeys3X2Aoc2ZbEpvjmAAAAAHnAcMFAA"  # Userbot StringSession

# 🔹 Başlatma
bot = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
user = Client(user_session, api_id=api_id, api_hash=api_hash)
pytg = PyTgCalls(user)

# 🔹 Şarkı oynatma fonksiyonu (indir → çal → sil)
async def play_music(chat_id, query):
    filename = "song.mp3"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "noplaylist": True,
        "quiet": True
    }

    # Link değilse YouTube'da ara
    if not query.startswith("http"):
        query = f"ytsearch1:{query}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        if "entries" in info:
            info = info["entries"][0]
        title = info.get("title", "Bilinmeyen Şarkı")
        duration = info.get("duration", 0)

    # Çal
    await pytg.join_group_call(chat_id, InputAudioStream(filename))
    # Çalma süresi boyunca bekle
    await asyncio.sleep(duration + 1)

    # Dosyayı sil
    if os.path.exists(filename):
        os.remove(filename)

    return title

# 🔹 /start komutu
@bot.on_message(filters.command("start"))
async def start(_, msg):
    if msg.chat.type == "private":
        await msg.reply(
            "👋 Merhaba!\n\n"
            "Ben bir 🎶 **Müzik Çalma Botuyum**.\n"
            "• Gruptaki sesli sohbetlere katılırım.\n"
            "• Şarkı ismi veya link yazarak müzik çaldırabilirsin.\n"
            "• Kontrol için butonları kullanabilirsin.\n\n"
            "ℹ️ Beni bir **gruba ekle** ve oradan kullanmaya başla."
        )
    else:
        await msg.reply(
            "🎶 Müzik Botuna Hoşgeldin!\n\nButonlardan seçim yapabilirsin:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🎵 Şarkı Oynat", callback_data="play")],
                    [
                        InlineKeyboardButton("⏸ Duraklat", callback_data="pause"),
                        InlineKeyboardButton("▶️ Devam", callback_data="resume"),
                    ],
                    [InlineKeyboardButton("⏭ Sonraki", callback_data="skip"),
                     InlineKeyboardButton("🛑 Durdur", callback_data="stop")],
                ]
            )
        )

# 🔹 Callback butonları
@bot.on_callback_query()
async def callbacks(_, cq):
    if cq.data == "play":
        await cq.message.edit("🎵 Çalmak istediğin şarkının **isim veya link**'ini yaz.")
    elif cq.data == "pause":
        await pytg.pause_stream(cq.message.chat.id)
        await cq.answer("⏸ Şarkı duraklatıldı")
    elif cq.data == "resume":
        await pytg.resume_stream(cq.message.chat.id)
        await cq.answer("▶️ Devam ediyor")
    elif cq.data == "stop":
        await pytg.leave_group_call(cq.message.chat.id)
        await cq.answer("🛑 Müzik durduruldu")
    elif cq.data == "skip":
        await cq.answer("⏭ Sonraki şarkı özelliği henüz yok.")

# 🔹 Kullanıcının yazdığı mesajla şarkı çalma
@bot.on_message(filters.text & ~filters.command("start"))
async def play_from_text(_, msg):
    query = msg.text.strip()
    await msg.reply("🔎 Şarkı aranıyor ve çalınıyor...")
    try:
        title = await play_music(msg.chat.id, query)
        await msg.reply(f"▶️ Çalınıyor: {title}\n✅ Şarkı çalındıktan sonra sunucudan silindi.")
    except Exception as e:
        await msg.reply(f"❌ Şarkı çalınamadı: {e}")

# 🔹 Başlat
async def main():
    await bot.start()
    await user.start()
    await pytg.start()
    print("✅ Bot ve Userbot çalışıyor...")
    await asyncio.get_event_loop().create_future()

asyncio.run(main())
