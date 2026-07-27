from telegram.ext import (
    MessageHandler,
    ConversationHandler,
    filters,
)

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
start))
app.add_handler(
    ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex("^➕ Shina qo'shish$"),
                add_tire_start
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
)
    print("Bot ishga tushdi...")

    app.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(init_db())
    main()
