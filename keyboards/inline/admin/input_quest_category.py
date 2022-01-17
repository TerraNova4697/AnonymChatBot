from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

input_category_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Без категории", callback_data="no_category")
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])
