from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin.admin_callback_datas import choose_openness_callback

choose_openness_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="Формальный", callback_data=choose_openness_callback
                             .new(action="openness", openness="Формальный")),
        InlineKeyboardButton(text="Приятельский", callback_data=choose_openness_callback
                             .new(action="openness", openness="Приятельский"))
    ],
    [
        InlineKeyboardButton(text="Дружеский", callback_data=choose_openness_callback
                             .new(action="openness", openness="Дружеский")),
        InlineKeyboardButton(text="Близость", callback_data=choose_openness_callback
                             .new(action="openness", openness="Близость"))
    ],
    [
        InlineKeyboardButton(text="Исповедь", callback_data=choose_openness_callback
                             .new(action="openness", openness="Исповедь")),
        InlineKeyboardButton(text="Отменить", callback_data="cancel")
    ]
])
