from telegram.ext import ConversationHandler

# ➕ Tovar qo'shish
NAME, PRICE, QUANTITY = range(3)

# ➖ Sotish
SELL_NAME, SELL_QUANTITY = range(3, 5)

# 🔍 Qidirish
SEARCH = 5

# ✏️ Tahrirlash
EDIT_SELECT, EDIT_PRICE, EDIT_QUANTITY = range(6, 9)

# 🗑️ O'chirish
DELETE = 9

# Conversation tugashi
END = ConversationHandler.END