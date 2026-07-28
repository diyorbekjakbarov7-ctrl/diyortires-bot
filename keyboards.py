from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    keyboard = [
        [
            KeyboardButton("📦 Ombor"),
            KeyboardButton("➕ Tovar qo'shish")
        ],
        [
            KeyboardButton("📥 Kirim"),
            KeyboardButton("📤 Chiqim")
        ],
        [
            KeyboardButton("📜 Tarix")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )