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
    await update.message.reply_text("🛞 Shina brendini kiriting:")
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
        await update.message.reply_text(
            "❌ Narxni faqat raqam bilan kiriting.\nMasalan: 95"
        )
        return PRICE

    await update.message.reply_text("📦 Soni nechta?")
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

    total = context.user_data["price"] * qty

    await update.message.reply_text(
        f"""✅ Shina qo'shildi!

🛞 {context.user_data["brand"]} {context.user_data["model"]}
📏 {context.user_data["size"]}
📅 DOT: {context.user_data["dot"]}
💵 Narxi: ${context.user_data["price"]}
📦 Soni: {qty}
💰 Jami: ${total}
"""
    )

    return ConversationHandler.END


async def show_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tires = await get_all_tires()

    if not tires:
        await update.message.reply_text("📦 Ombor hozircha bo'sh.")
        return

    text = "📦 Ombordagi shinalar\n\n"

    total_quantity = 0
    total_value = 0

    for tire in tires:
        tire_id, brand, model, size, dot, price, quantity = tire

        total_quantity += quantity
        total_value += price * quantity

        text += (
            f"🆔 ID: {tire_id}\n"
            f"🛞 {brand} {model}\n"
            f"📏 {size}\n"
            f"📅 DOT: {dot}\n"
            f"💵 ${price}\n"
            f"📦 {quantity} dona\n"
            f"💰 ${price * quantity}\n"
            "------------------------\n"
        )

    text += (
        f"\n📦 Jami shina: {total_quantity} dona\n"
        f"💰 Umumiy qiymat: ${total_value}"
    )

    await update.message.reply_text(text)