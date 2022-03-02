from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.user.callback_datas import partner_found_callback


def create_keyboard_found_partner(partners_user_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Принять", callback_data="accept")
        ],
        [
            InlineKeyboardButton(text="Отклонить", callback_data="deny")
        ]
    ])
    return keyboard
