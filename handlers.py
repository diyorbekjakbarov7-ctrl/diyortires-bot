from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from states import (
    NAME,
    PRICE,
    QUANTITY,
    SELL_NAME,
    SELL_QUANTITY
)

from database import (
    add_product,
    get_products,
    sell_product
    get_history
)


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

    text = update.message.text.replace("$", "").replace(" ", "")

    try:
        price = int(text)
    except:
        await update.message.reply_text(
            "❌ Narx noto'g'ri"
        )
        return PRICE


    context.user_data["price"] = price

    await update.message.reply_text(
        "🔢 Soni kiriting:"
    )

    return QUANTITY


async def product_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):

    quantity = int(update.message.text)

    add_product(
        context.user_data["name"],
        context.user_data["price"],
        quantity
    )

    await update.message.reply_text(
        "✅ Tovar qo'shildi"
    )

    context.user_data.clear()

    return ConversationHandler.END



async def show_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):

    products = get_products()

    if not products:
        await update.message.reply_text(
            "📦 Ombor bo'sh"
        )
        return


    text = "📦 Ombor:\n\n"

    for p in products:
        text += (
            f"🛞 {p['name']}\n"
            f"💰 {p['price']}\n"
            f"🔢 {p['quantity']} dona\n\n"
        )

    await update.message.reply_text(text)



async def sell_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🛞 Sotilgan shina nomini kiriting:"
    )

    return SELL_NAME



async def sell_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["sell_name"] = update.message.text

    await update.message.reply_text(
        "🔢 Nechta sotildi?"
    )

    return SELL_QUANTITY



async def sell_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):

    quantity = int(update.message.text)

    success, result = sell_product(
        context.user_data["sell_name"],
        quantity
    )


    if success:
        await update.message.reply_text(
            f"✅ Ombor yangilandi\n\n"
            f"Qoldi: {result} dona"
        )

    else:
        await update.message.reply_text(
            f"❌ {result}"
        )


    context.user_data.clear()

    return ConversationHandler.END
    async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):

    history = get_history()

    if not history:
        await update.message.reply_text(
            "📜 Tarix bo'sh."
        )
        return


    text = "📜 Tarix:\n\n"


    for item in history:

        if item["action"] == "ADD":
            action = "➕ Qo'shildi"
        else:
            action = "➖ Sotildi"


        text += (
            f"{action}\n"
            f"🛞 {item['name']}\n"
            f"🔢 {item['quantity']} dona\n"
            f"📅 {item['created_at']}\n\n"
        )


    await update.message.reply_text(text)