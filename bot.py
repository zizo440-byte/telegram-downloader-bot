import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي رابط الفيديو وأنا أحمله لك\nالحد الأقصى للإرسال: 50 ميقا\nأكبر من كذا يرسل لك رابط تحميل")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("جاري فحص الفيديو...")

    try:
        ydl_opts = {
            'format': 'best[filesize<50M][ext=mp4]/best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'الفيديو')
            filesize = info.get('filesize') or info.get('filesize_approx', 0)
            video_url = info.get('url')

        size_mb = round(filesize / 1024 / 1024, 2) if filesize else 0

        if filesize and filesize > 50 * 1024 * 1024:
            await msg.edit_text(f"**{title}**\nالحجم: {size_mb} ميقا\nأكبر من 50 ميقا، هذا رابط التحميل المباشر:\n{video_url}")
        else:
            await msg.edit_text("جاري الإرسال...")
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url, caption=title)
            await msg.delete()

    except Exception as e:
        await msg.edit_text(f"صار خطأ: {e}")

def main():
    if not TOKEN:
        print("خطأ: TOKEN مو موجود")
        return
    app
