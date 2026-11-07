from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, Message


def number_button():
    button = [
        [
            KeyboardButton(text="Поделиться контактом",request_contact=True)
        ]
    ]
    return ReplyKeyboardMarkup(
        keyboard=button,
        resize_keyboard=True,
        one_time_keyboard=True
    )