from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin.admin_callback_datas import edit_question_keyboard


def create_edit_question_keyboard(question_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить вопрос", callback_data=edit_question_keyboard
                                 .new(action="edit_question", question_id=str(question_id)))
        ],
        [
            InlineKeyboardButton(text="Изменить категорию", callback_data=edit_question_keyboard
                                 .new(action="edit_cat", question_id=str(question_id)))
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="to_questions")
        ]
    ])
    return keyboard
