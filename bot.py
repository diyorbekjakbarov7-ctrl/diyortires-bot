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

    show_stock,

    sell_start,
    sell_name,
    sell_quantity,

    show_history,

    search_start,
    search_result,

    edit_start,
    edit_select,
    edit_price,
    edit_quantity,

    delete_start,
    delete_confirm
)

from states import (
    NAME,
    PRICE,
    QUANTITY,

    SELL_NAME,
    SELL_QUANTITY,

    SEARCH,

    EDIT_SELECT,
    EDIT_PRICE,
    EDIT_QUANTITY,

    DELETE
)


# Render uchun
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
        "🛞 Diyortires Ombor Bot\n\n"
        "Kerakli bo'limni tanlang:",
        reply_markup=main_menu()
    )


async def run_bot():

    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()


    # /start
    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    # 📦 Ombor
    app.add_handler(
        MessageHandler(
            filters.Regex("^📦 Ombor$"),
            show_stock
        )
    )


    # 📜 Tarix
    app.add_handler(
        MessageHandler(
            filters.Regex("^📜 Tarix$"),
            show_history
        )
    )


    # ➕ Tovar qo'shish
    add_handler = ConversationHandler(

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
            ]

        },

        fallbacks=[]
    )


    app.add_handler(add_handler)


    # ➖ Sotildi
    sell_handler = ConversationHandler(

        entry_points=[
            MessageHandler(
                filters.Regex("^➖ Sotildi$"),
                sell_start
            )
        ],

        states={

            SELL_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    sell_name
                )
            ],

            SELL_QUANTITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    sell_quantity
                )
            ]

        },

        fallbacks=[]
    )


    app.add_handler(sell_handler)


    # 🔍 Qidirish
    search_handler = ConversationHandler(

        entry_points=[
            MessageHandler(
                filters.Regex("^🔍 Qidirish$"),
                search_start
            )
        ],

        states={

            SEARCH: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    search_result
                )
            ]

        },

        fallbacks=[]
    )


    app.add_handler(search_handler)


    # ✏️ Tahrirlash
    edit_handler = ConversationHandler(

        entry_points=[
            MessageHandler(
                filters.Regex("^✏️ Tahrirlash$"),
                edit_start
            )
        ],

        states={

            EDIT_SELECT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_select
                )
            ],

            EDIT_PRICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_price
                )
            ],

            EDIT_QUANTITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    edit_quantity
                )
            ]

        },

        fallbacks=[]
    )


    app.add_handler(edit_handler)


    # 🗑 O'chirish
    delete_handler = ConversationHandler(

        entry_points=[
            MessageHandler(
                filters.Regex("^🗑️ O'chirish$"),
                delete_start
            )
        ],

        states={

            DELETE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    delete_confirm
                )
            ]

        },

        fallbacks=[]
    )


    app.add_handler(delete_handler)


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