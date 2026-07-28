import asyncio
import threading

from flask import Flask
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
    product_quantity,
    show_stock
)

from states import NAME, PRICE, QUANTITY


# Render uchun web server
web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Diyortires bot ishlayapti!"


def run_web():
    web_app.run(
        host="0.0.0.0",
        port=10000
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛞 Avtoshina Ombor Botiga xush kelibsiz!\n\n"
        "Kerakli bo'limni tanlang:",
        reply_markup=main_menu()
    )


async def run_bot():
    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    add_product_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^➕ Tovar qo'shish$"),
                add_product_start
            )
        ],

        states={
            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    product_name
                )
            ],

            PRICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    product_price
                )
            ],

            QUANTITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    product_quantity
                )
            ],
        },

        fallbacks=[]
    )

    app.add_handler(add_product_handler)

    print("Bot ishga tushdi...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    await asyncio.Event().wait()


def main():
    threading.Thread(
        target=run_web,
        daemon=True
    ).start()

    asyncio.run(run_bot())


if __name__ == "__main__":
    main()