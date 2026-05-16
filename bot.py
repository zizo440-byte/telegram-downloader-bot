import os
import yt_dlp
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text("هلا! البوت شغال ✅")

async def handle_tiktok(update, context):
    url = update.message.text
    msg = await update.message.reply_text("جاري التحميل... ⏳")

    try:
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'mp4',
            'noplaylist': True,
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await context.bot.send_video(chat_id=update.effective_chat.id, video=open('video.mp4', 'rb'))
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"صار خطأ في التحميل:\n{e}")

def main():
    token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("tiktok.com"), handle_tiktok))
    app.run_polling()

if __name__ == "__main__":
    main()
