from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from config import BOT_TOKEN
from keyboards import main_menu
from database import create_tables


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛞 Avtoshina Ombor Botiga xush kelibsiz!\n\n"
        "Kerakli bo'limni tanlang:",
        reply_markup=main_menu()
    )


def main():
    # Bazani yaratish
    create_tables()

    # Botni ishga tushirish
    app = Application.builder().token(BOT_TOKEN).build()

    # /start
    app.add_handler(CommandHandler("start", start))

    print("Bot ishga tushdi...")

    app.run_polling()


if __name__ == "__main__":
    main()