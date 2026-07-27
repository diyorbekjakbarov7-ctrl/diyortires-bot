from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN
from database import init_db
from keyboards import main_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 Diyor Tires ombor botiga xush kelibsiz!",
        reply_markup=main_keyboard
    )


def main():
    app = Application.builder().token(8268094538:AAEClCd1BrDtd92lZ6YAoz4MoJX-QjnHfDs
).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot ishga tushdi...")

    app.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(init_db())
    main()
