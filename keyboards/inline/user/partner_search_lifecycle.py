from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.user.callback_datas import partner_found_callback


def create_keyboard_found_partner(partners_user_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Принять", callback_data="accept_partn")
        ],
        [
            InlineKeyboardButton(text="Отклонить", callback_data="deny_partn")
        ]
    ])
    return keyboard


def create_keyboard_back_to_partner_search():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Отменить", callback_data="cancel_partner")
        ]
    ])
    return keyboard
