import os
import yt_dlp
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text("هلا! أرسل لي رابط تيك توك أو يوتيوب وأنزله لك ✅")

import requests

async def handle_tiktok(update, context):
    url = update.message.text
    msg = await update.message.reply_text("جاري جلب رابط التحميل...")

    try:
        api_url = f"https://ytapi.me/api/video/info?url={url}"
        r = requests.get(api_url, timeout=20)

        if r.status_code != 200:
            await msg.edit_text(f"الـ API رفض الطلب: {r.status_code}")
            return

        data = r.json()

        if not data.get("success") or not data.get("url"):
            await msg.edit_text("ما قدرت أجيب الرابط، جرب رابط ثاني")
            return

        video_url = data["url"]
        title = data.get("title", "الفيديو")

        await msg.edit_text(
            f"✅ **{title}**\n\n"
            f"الرابط المباشر جاهز:\n{video_url}\n\n"
            f"افتحه من المتصفح وبيحمل معك.",
            parse_mode='Markdown'
        )

    except Exception as e:
        await msg.edit_text(f"صار خطأ:\n{e}")

def main():
    token = os.getenv("BOT_TOKEN")
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("tiktok.com|youtube.com|youtu.be"), handle_tiktok))
    app.run_polling()

if __name__ == "__main__":
    main()
