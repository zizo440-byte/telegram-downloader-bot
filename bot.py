import os
import yt_dlp
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text("هلا! أرسل لي رابط تيك توك أو يوتيوب وأنزله لك ✅")

async def handle_tiktok(update, context):
    url = update.message.text
    msg = await update.message.reply_text("جاري التحميل... ⏳")
try:
    ydl_opts = {
        'format': 'mp4/best[filesize<500M]',
        'quiet': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android'],
            }
        },
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_url = info['url']
        title = info.get('title', 'الفيديو')
    
    await msg.edit_text(
        f"✅ **{title}**\n\n"
        f"الرابط المباشر جاهز:\n{video_url}\n\n"
        f"افتحه من المتصفح وبيحمل معك بأي حجم.",
        parse_mode='Markdown'
    )
    
except Exception as e:
    await msg.edit_text(f"صار خطأ في التحميل:\n{e}")
        await msg.edit_text(f"صار خطأ في التحميل:\n{e}")

def main():
    token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("tiktok.com|youtube.com|youtu.be"), handle_tiktok))
    app.run_polling()

if __name__ == "__main__":
    main()
