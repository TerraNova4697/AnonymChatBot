from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

continue_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Продолжить", callback_data="continue")
    ]
])

accept_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Принять", callback_data="accept")
    ]
])

try_again_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Попробовать еще раз", callback_data="accept")
    ]
])
