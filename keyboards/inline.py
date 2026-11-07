from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def fac_buttons(faculties):
    builder = InlineKeyboardBuilder()
    for faculty in faculties:
        builder.button(
            text=faculty,
            callback_data=f"faculty:{faculty}"
        )
        builder.adjust(2)
    return builder.as_markup()
def applay_buttons():
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data="yes"),
            InlineKeyboardButton(text="Нет, пройти регестрацию занаво ", callback_data="no")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
