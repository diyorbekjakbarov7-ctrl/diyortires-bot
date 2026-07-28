from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database import (
    add_product,
    get_products,
    sell_product,
    get_history,
    search_product,
    update_product,
    delete_product
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


# ==========================
# ➕ TOVAR QO'SHISH
# ==========================

async def add_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛞 Tovar nomini kiriting:"
    )
    return NAME


async def product_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    name = update.message.text.strip()

    if len(name) < 2:
        await update.message.reply_text(
            "❌ Nom juda qisqa. Qayta kiriting:"
        )
        return NAME

    context.user_data["name"] = name

    await update.message.reply_text(
        "💰 Narxini kiriting:"
    )

    return PRICE


async def product_price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        price = float(
            update.message.text.replace(",", ".")
        )

        if price <= 0:
            raise ValueError

    except:
        await update.message.reply_text(
            "❌ Narx noto'g'ri. Masalan: 500000"
        )
        return PRICE


    context.user_data["price"] = price

    await update.message.reply_text(
        "📦 Miqdorini kiriting:"
    )

    return QUANTITY


async def product_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        quantity = int(update.message.text)

        if quantity <= 0:
            raise ValueError

    except:
        await update.message.reply_text(
            "❌ Miqdor noto'g'ri. Masalan: 10"
        )
        return QUANTITY


    add_product(
        context.user_data["name"],
        context.user_data["price"],
        quantity
    )


    await update.message.reply_text(
        "✅ Tovar qo'shildi."
    )

    context.user_data.clear()

    return ConversationHandler.END



# ==========================
# 📦 OMBOR
# ==========================

async def show_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):

    products = get_products()

    if not products:
        await update.message.reply_text(
            "📦 Ombor bo'sh."
        )
        return


    text = "📦 Ombor:\n\n"


    for p in products:
        text += (
            f"🛞 {p['name']}\n"
            f"💰 {p['price']}\n"
            f"📦 {p['quantity']} dona\n\n"
        )


    await update.message.reply_text(text)



# ==========================
# ➖ SOTILDI
# ==========================

async def sell_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🛞 Sotilgan tovar nomini kiriting:"
    )

    return SELL_NAME


async def sell_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["sell_name"] = update.message.text.strip()

    await update.message.reply_text(
        "📦 Nechta sotildi?"
    )

    return SELL_QUANTITY


async def sell_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        quantity = int(update.message.text)

    except:
        await update.message.reply_text(
            "❌ Son kiriting."
        )
        return SELL_QUANTITY


    ok, message = sell_product(
        context.user_data["sell_name"],
        quantity
    )


    await update.message.reply_text(message)

    context.user_data.clear()

    return ConversationHandler.END
    # ==========================
# 📜 TARIX
# ==========================

async def show_history(update: Update, context: ContextTypes.DEFAULT_TYPE):

    history = get_history()

    if not history:
        await update.message.reply_text(
            "📜 Tarix bo'sh."
        )
        return


    text = "📜 Tarix:\n\n"


    for item in history:

        action = (
            "➕ Qo'shildi"
            if item["action"] == "ADD"
            else "➖ Sotildi"
        )

        text += (
            f"{action}\n"
            f"🛞 {item['name']}\n"
            f"📦 {item['quantity']} dona\n"
            f"🕒 {item['created_at']}\n\n"
        )


    await update.message.reply_text(text)



# ==========================
# 🔍 QIDIRISH
# ==========================

async def search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔍 Tovar nomini kiriting:"
    )

    return SEARCH



async def search_result(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyword = update.message.text.strip()

    products = search_product(keyword)


    if not products:
        await update.message.reply_text(
            "❌ Tovar topilmadi."
        )
        return ConversationHandler.END


    text = "🔍 Natija:\n\n"


    for p in products:

        text += (
            f"🆔 ID: {p['id']}\n"
            f"🛞 {p['name']}\n"
            f"💰 {p['price']}\n"
            f"📦 {p['quantity']} dona\n\n"
        )


    await update.message.reply_text(text)

    return ConversationHandler.END



# ==========================
# ✏️ TAHRIRLASH
# ==========================

async def edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "✏️ Tahrirlash uchun ID kiriting:"
    )

    return EDIT_SELECT



async def edit_select(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        product_id = int(update.message.text)

    except:
        await update.message.reply_text(
            "❌ ID raqam bo'lishi kerak."
        )
        return EDIT_SELECT


    context.user_data["edit_id"] = product_id


    await update.message.reply_text(
        "💰 Yangi narxni kiriting:"
    )

    return EDIT_PRICE



async def edit_price(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        price = float(update.message.text)

    except:
        await update.message.reply_text(
            "❌ Narx noto'g'ri."
        )
        return EDIT_PRICE


    context.user_data["edit_price"] = price


    await update.message.reply_text(
        "📦 Yangi miqdorni kiriting:"
    )

    return EDIT_QUANTITY



async def edit_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        quantity = int(update.message.text)

    except:
        await update.message.reply_text(
            "❌ Miqdor noto'g'ri."
        )
        return EDIT_QUANTITY


    update_product(
        context.user_data["edit_id"],
        context.user_data["edit_price"],
        quantity
    )


    await update.message.reply_text(
        "✅ Tovar yangilandi."
    )


    context.user_data.clear()

    return ConversationHandler.END



# ==========================
# 🗑 O'CHIRISH
# ==========================

async def delete_start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🗑 O'chirish uchun ID kiriting:"
    )

    return DELETE



async def delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        product_id = int(update.message.text)

    except:
        await update.message.reply_text(
            "❌ ID raqam bo'lishi kerak."
        )
        return DELETE


    delete_product(product_id)


    await update.message.reply_text(
        "✅ Tovar o'chirildi."
    )


    return ConversationHandler.END