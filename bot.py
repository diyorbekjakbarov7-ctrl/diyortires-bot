from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from database import init_db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "Diyor Tires ombor botiga xush kelibsiz.\n\n"
        "Bot tayyorlanmoqda..."
    )


async def main():
    await init_db()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot ishga tushdi...")

    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
