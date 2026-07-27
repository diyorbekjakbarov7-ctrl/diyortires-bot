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
    async def dot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["dot"] = update.message.text
    await update.message.reply_text("💵 1 dona narxini kiriting (USD):")
    return PRICE


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["price"] = float(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Narxni faqat raqam bilan kiriting. Masalan: 95")
        return PRICE

    await update.message.reply_text("📦 Ombordagi sonini kiriting:")
    return QUANTITY


async def quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        qty = int(update.message.text)
    except ValueError:
        await update.message.reply_text("❌ Sonni faqat raqam bilan kiriting.")
        return QUANTITY

    await add_tire(
        context.user_data["brand"],
        context.user_data["model"],
        context.user_data["size"],
        context.user_data["dot"],
        context.user_data["price"],
        qty,
    )

    await update.message.reply_text(
        "✅ Shina muvaffaqiyatli qo'shildi!"
    )

    return ConversationHandler.END