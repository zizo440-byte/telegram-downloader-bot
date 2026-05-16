import os
from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text("هلا! البوت شغال ✅")

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise ValueError("BOT_TOKEN not set")
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
