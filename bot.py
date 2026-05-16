from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي رابط تيك توك أو يوتيوب وأنزله لك 🎥")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not ("youtube.com" in url or "youtu.be" in url or "tiktok.com" in url):
        await update.message.reply_text("أرسل رابط يوتيوب أو تيك توك فقط")
        return
    
    msg = await update.message.reply_text("جاري التحميل...")
    
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best[filesize<50M]',
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)
        
        await msg.edit_text("تم التحميل، جاري الإرسال...")
        await update.message.reply_video(video=open(file, 'rb'))
        os.remove(file)
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"فشل التحميل: {str(e)}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

print("Bot is running...")
app.run_polling()