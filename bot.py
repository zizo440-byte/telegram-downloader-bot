import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا فيك! ارسل لي رابط الفيديو وانا انزله لك")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("جاري التحميل...")

    try:
        api_url = "https://api.cobalt.tools/api/json"
        payload = {
            "url": url,
            "videoQuality": "720",
            "audioFormat": "mp4",
            "audioBitrate": "128"
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(api_url, json=payload, headers=headers)

        if r.status_code != 200:
            await msg.edit_text(f"الـ API رفض الطلب: {r.status_code}")
            return
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("جاري التحميل...")

    try:
        api_url = "https://api.cobalt.tools/api/json"
        payload = {
            "url": url,
            "videoQuality": "720",
            "audioFormat": "mp4",
            "audioBitrate": "128"
        }
        headers = {"Content-Type": "application/json"}
        r = requests.post(api_url, json=payload, headers=headers)

        if r.status_code != 200:
            await msg.edit_text(f"الـ API رفض الطلب: {r.status_code}")
            return

        data = r.json()

        if data.get("status") not in ["stream", "success"]:
            await msg.edit_text("ما قدرت اجيب الرابط")
            return

        video_url = data.get("url")
        await msg.edit_text("تم جلب الرابط بنجاح")
        await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url)

    except Exception as e:
        await msg.edit_text(f"صار خطأ: {e}")
        await msg.edit_text(f"صار خطأ: {e}")
