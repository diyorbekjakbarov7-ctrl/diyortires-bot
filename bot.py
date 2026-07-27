from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    ConversationHandler,
    filters,
)

from config import BOT_TOKEN
from database import init_db
from keyboards import main_keyboard
from handlers import (
    add_tire_start,
    brand,
    model,
    size,
    dot,
    price,
    quantity,
    BRAND,
    MODEL,
    SIZE,
    DOT,
    PRICE,
    QUANTITY,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏠 Diyor Tires ombor botiga xush kelibsiz!",
        reply_markup=main_keyboard
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^➕ Shina qo'shish$"),
                add_tire_start,
            )
        ],
        states={
            BRAND: [MessageHandler(filters.TEXT & ~filters.COMMAND, brand)],
            MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, model)],
            SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, size)],
            DOT: [MessageHandler(filters.TEXT & ~filters.COMMAND, dot)],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, price)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, quantity)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

    print("Bot ishga tushdi...")

    app.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(init_db())
    main()