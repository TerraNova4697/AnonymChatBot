from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin.admin_callback_datas import edit_f_question_callback


def create_edit_f_question_keyboard(f_question_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton(text="Добавить варианты ответов", callback_data=edit_f_question_callback
                                         .new(action="add_option", f_question_id=str(f_question_id))))
    keyboard.row(InlineKeyboardButton(text="Завершить", callback_data=edit_f_question_callback
                                      .new(action="finish", f_question_id=str(f_question_id))))
    keyboard.insert(InlineKeyboardButton(text="Назад", callback_data="to_f_questions"))
    keyboard.row(InlineKeyboardButton(text="Удалить вопрос", callback_data="delete_f_question"))
    return keyboard
