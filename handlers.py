from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from states import NAME, PRICE, QUANTITY
from database import add_product


async def add_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Tovar nomini kiriting:"
    )
    return NAME


async def product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text

    await update.message.reply_text(
        "💰 Narxini kiriting:"
    )

    return PRICE


async def product_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["price"] = int(update.message.text)

    await update.message.reply_text(
        "🔢 Soni kiriting:"
    )

    return QUANTITY


async def product_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quantity = int(update.message.text)

    name = context.user_data["name"]
    price = context.user_data["price"]

    add_product(
        name,
        price,
        quantity
    )

    await update.message.reply_text(
        "✅ Tovar qo'shildi\n\n"
        f"Nomi: {name}\n"
        f"Narxi: {price} so'm\n"
        f"Soni: {quantity} dona"
    )

    context.user_data.clear()

    return ConversationHandler.END