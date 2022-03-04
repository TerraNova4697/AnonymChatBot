from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.user.callback_datas import partner_found_callback, choose_openness_callback


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


def create_keyboard_choose_openness():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Формальный", callback_data=choose_openness_callback.new(action="openness",
                                                                                               choice="Формальный"))
        ],
        [
            InlineKeyboardButton(text="Приятельский", callback_data=choose_openness_callback.new(action="openness",
                                                                                                 choice="Приятельский"))
        ],
        [
            InlineKeyboardButton(text="Дружеский", callback_data=choose_openness_callback.new(action="openness",
                                                                                              choice="Дружеский"))
        ],
        [
            InlineKeyboardButton(text="Близость", callback_data=choose_openness_callback.new(action="openness",
                                                                                             choice="Близость"))
        ],
        [
            InlineKeyboardButton(text="Исповедь", callback_data=choose_openness_callback.new(action="openness",
                                                                                             choice="Исповедь"))
        ],
    ])
    return keyboard


def create_keyboard_accept_partners_openness():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Согласен", callback_data="accept_level")
        ],
        [
            InlineKeyboardButton(text="Начать поиск собеседника", callback_data="search_partner")
        ]
    ])
    return keyboard


def create_keyboard_search_new_partner():
    keyword = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Начать поиск собеседника", callback_data="search_partner")
        ]
    ])
    return keyword
