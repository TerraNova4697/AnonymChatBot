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

go_on_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Перейти", callback_data="go_on")
    ]
])

fill_in_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Заполнить", callback_data="fill_in")
    ]
])

begin_search = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Начать поиск собеседника", callback_data="begin_search")
    ]
])
