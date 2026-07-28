from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = [
        [
            KeyboardButton("➕ Tovar qo'shish"),
            KeyboardButton("📦 Ombor"),
        ],
        [
            KeyboardButton("➖ Sotildi"),
            KeyboardButton("📜 Tarix"),
        ],
        [
            KeyboardButton("🔍 Qidirish"),
            KeyboardButton("✏️ Tahrirlash"),
        ],
        [
            KeyboardButton("🗑️ O'chirish"),
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )