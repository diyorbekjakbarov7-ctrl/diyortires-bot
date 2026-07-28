from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from database import add_tire, get_all_tires

(
    BRAND,
    MODEL,
    SIZE,
    DOT,
    PRICE,
    QUANTITY,
) = range(6)


async def add_tire_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "🛞 Shina brendini kiriting:"
    )

    return BRAND


async def brand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["brand"] = update.message.text
    await update.message.reply_text("📝 Modelni kiriting:")
    return MODEL


async def model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["model"] = update.message.text
    await update.message.reply_text("📏 Razmerni kiriting:")
    return SIZE