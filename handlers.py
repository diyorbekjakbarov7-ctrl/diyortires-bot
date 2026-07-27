from telegram import Update
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database import add_tire

(
    BRAND,
    MODEL,
    SIZE,
    DOT,
    PRICE,
    QUANTITY,
) = range(6)


async def add_tire_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛞 Shina brendini kiriting:\n\nMisol: Michelin"
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


async def size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["size"] = update.message.text
    await update.message.reply_text("📅 DOT ni kiriting:")
    return DOT