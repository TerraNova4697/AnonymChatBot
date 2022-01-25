from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

edit_test_question_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Завершить", callback_data="finish")
    ],
    [
        InlineKeyboardButton(text="Добавить правильный овтет", callback_data="add_correct")
    ],
    [
        InlineKeyboardButton(text="Добавить неправильный ответ", callback_data="add_incorrect")
    ],
    [
        InlineKeyboardButton(text="Отмена", callback_data="cancel")
    ]
])
