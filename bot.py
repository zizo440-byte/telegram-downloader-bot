import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text("هلا! البوت شغال ✅")

async def handle_tiktok(update, context):
    url = update.message.text
    await update.message.reply_text(f"استلمت رابط التيك توك:\n{url}\n\nالحين أحمله لك...")
    # هنا تحط كود التحميل لاحقاً

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not set")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("tiktok.com"), handle_tiktok))
    app.run_polling()

if __name__ == "__main__":
    main()
