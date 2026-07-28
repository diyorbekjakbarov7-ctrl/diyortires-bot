from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)

from config import BOT_TOKEN
from keyboards import main_menu
from database import create_tables

from handlers import (
    add_product_start,
    product_name,
    product_price,
    product_quantity
)

from states import NAME, PRICE, QUANTITY


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


import asyncio


async def run():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot ishga tushdi...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(run())