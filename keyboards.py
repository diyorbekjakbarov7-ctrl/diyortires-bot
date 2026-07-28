from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_menu():

    keyboard = [
        [
            KeyboardButton("➕ Tovar qo'shish"),
            KeyboardButton("📦 Ombor")
        ],
        [
            KeyboardButton("➖ Sotildi"),
            KeyboardButton("📜 Tarix")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )