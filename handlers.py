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
    DELETE,
    END
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
            "❌ Tovar nomi juda qisqa.\n\nQayta kiriting:"
        )
        return NAME
    context.user_data["name"] = name
    await update.message.reply_text(
        "💰 Narxini kiriting:"
    )
    return PRICE
async def product_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace(" ", "").replace(",", ".")
    try:
        price = float(text)
        if price <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text(
            "❌ Narx noto'g'ri.\n\nMasalan:\n500000"
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
    except ValueError:
        await update.message.reply_text(
            "❌ Miqdor noto'g'ri.\n\nMasalan:\n10"
        )
        return QUANTITY
    add_product(
        context.user_data["name"],
        context.user_data["price"],
        quantity
    )
    await update.message.reply_text(
        "✅ Mahsulot muvaffaqiyatli qo'shildi."
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
    text = "📦 Ombordagi mahsulotlar:\n\n"
    for product in products:
        text += (
            f"🛞 {product['name']}\n"
            f"💰 {product['price']}\n"
            f"📦 {product['quantity']} dona\n\n"
        )
    await update.message.reply_text(text)
# ==========================
# ➖ SOTILDI
# ==========================
async def sell_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛞 Sotilgan mahsulot nomini kiriting:"
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
        if quantity <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text(
            "❌ Miqdor noto'g'ri.\n\nMasalan: 2"
        )
        return SELL_QUANTITY
    success, message = sell_product(
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
        await update.message.reply_text("📜 Tarix bo'sh.")
        return
    text = "📜 Oxirgi amallar:\n\n"
    for item in history:
        action = "➕ Qo'shildi" if item["action"] == "ADD" else "➖ Sotildi"
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
        "🔍 Qidiriladigan mahsulot nomini kiriting:"
    )
    return SEARCH
async def search_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyword = update.message.text.strip()
    products = search_product(keyword)
    if not products:
        await update.message.reply_text("❌ Hech narsa topilmadi.")
        return ConversationHandler.END
    text = "🔍 Natijalar:\n\n"
    for product in products:
        text += (
            f"🆔 {product['id']}\n"
            f"🛞 {product['name']}\n"
            f"💰 {product['price']}\n"
            f"📦 {product['quantity']} dona\n\n"
        )
    await update.message.reply_text(text)
    return ConversationHandler.END
# ==========================
# ✏️ TAHRIRLASH
# ==========================
async def edit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✏️ Mahsulot ID raqamini kiriting:"
    )
    return EDIT_SELECT
async def edit_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["edit_id"] = int(update.message.text)
    await update.message.reply_text(
        "💰 Yangi narxni kiriting:"
    )
    return EDIT_PRICE
async def edit_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["edit_price"] = float(update.message.text)
    await update.message.reply_text(
        "📦 Yangi miqdorni kiriting:"
    )
    return EDIT_QUANTITY
async def edit_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update_product(
        context.user_data["edit_id"],
        context.user_data["edit_price"],
        int(update.message.text)
    )
    await update.message.reply_text(
        "✅ Mahsulot yangilandi."
    )
    context.user_data.clear()
    return ConversationHandler.END
# ==========================
# 🗑 O'CHIRISH
# ==========================
async def delete_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🗑 O'chiriladigan mahsulot ID sini kiriting:"
    )
    return DELETE
async def delete_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    delete_product(int(update.message.text))
    await update.message.reply_text(
        "✅ Mahsulot o'chirildi."
    )
    return ConversationHandler.END
``