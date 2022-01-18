from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin.admin_callback_datas import delete_question_callback


def create_question_deletion_keyboard(question_id):
    f_question_deletion_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
        [
            InlineKeyboardButton(text="Да, удалить", callback_data=delete_question_callback
                                 .new(action="delete", question_id=int(question_id))),
            InlineKeyboardButton(text="Отменить", callback_data=delete_question_callback
                                 .new(action="cancel", question_id=int(question_id)))
        ]
    ])
    return f_question_deletion_keyboard
