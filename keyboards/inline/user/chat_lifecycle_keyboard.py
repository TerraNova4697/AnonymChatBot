from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard_pass_question():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Пропустить", callback_data="pass_question")
        ]
    ])
    return keyboard


def create_keyboard_answered_all_questions():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Готов", callback_data="ready_lvl_up")
        ],
        [
            InlineKeyboardButton(text="Не готов", callback_data="not_ready")
        ]
    ])
    return keyboard
