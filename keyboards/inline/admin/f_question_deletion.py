from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

f_question_deletion_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text="Да, удалить", callback_data="confirmed"),
        InlineKeyboardButton(text="Отменить", callback_data="cancel_deletion")
    ]
])
