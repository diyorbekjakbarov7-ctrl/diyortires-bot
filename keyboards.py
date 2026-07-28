from telegram import ReplyKeyboardMarkup, KeyboardButton


def main_menu():

    keyboard = [
        [
            KeyboardButton("➕ Tovar qo'shish"),
            KeyboardButton("📦 Ombor")
        ],
        [
            KeyboardButton("➖ Sotildi")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )