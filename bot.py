import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل لي رابط فيديو يوتيوب وبنزله لك 📥")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("جاري التحميل...")

    try:
        ydl_opts = {
            'format': 'best[filesize<50M][ext=mp4]/best[ext=mp4]',
            'quiet': True,
            'no_warnings': True,
            'outtmpl': 'video.%(ext)s'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        await msg.delete()
        await update.message.reply_video(video=open(filename, 'rb'), caption=info.get('title', ''))
        
        os.remove(filename)
        
    except Exception as e:
        await msg.edit_text(f"صار خطأ: {str(e)}")

def main():
    if not TOKEN:
        print("Error: TOKEN not found. Set TOKEN in Environment Variables")
        return
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
