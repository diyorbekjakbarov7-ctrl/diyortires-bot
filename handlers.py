from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from states import NAME, PRICE, QUANTITY
from database import add_product, get_products


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
    text = update.message.text.strip()

    try:
        price = int(
            text.replace("$", "")
                .replace(" ", "")
                .replace(",", "")
        )

    except ValueError:
        await update.message.reply_text(
            "❌ Narx noto'g'ri.\n\n"
            "Misol:\n"
            "45$\n"
            "850000"
        )
        return PRICE

    context.user_data["price"] = price

    await update.message.reply_text(
        "🔢 Soni kiriting:"
    )

    return QUANTITY


async def product_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        quantity = int(update.message.text)

    except ValueError:
        await update.message.reply_text(
            "❌ Son faqat raqam bo'lishi kerak.\n"
            "Misol: 10"
        )
        return QUANTITY

    name = context.user_data["name"]
    price = context.user_data["price"]

    add_product(
        name,
        price,
        quantity
    )

    await update.message.reply_text(
        "✅ Tovar qo'shildi\n\n"
        f"🛞 Nomi: {name}\n"
        f"💰 Narxi: {price}\n"
        f"🔢 Soni: {quantity} dona"
    )

    context.user_data.clear()

    return ConversationHandler.END



async def show_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):

    products = get_products()

    if not products:
        await update.message.reply_text(
            "📦 Ombor bo'sh."
        )
        return

    text = "📦 Ombor:\n\n"

    for product in products:
        text += (
            f"🛞 {product['name']}\n"
            f"💰 Narxi: {product['price']}\n"
            f"🔢 Soni: {product['quantity']} dona\n\n"
        )

    await update.message.reply_text(text)