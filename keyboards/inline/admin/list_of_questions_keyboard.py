from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin.admin_callback_datas import choose_question_callback


def create_list_of_questions_keyboard(questions):
    keyboard = InlineKeyboardMarkup(row_width=5)
    for num, question in enumerate(questions):
        keyboard.insert(InlineKeyboardButton(text=str(num+1), callback_data=choose_question_callback
                                             .new(action="choose_quest", question_id=str(question[0]))))
    keyboard.row(InlineKeyboardButton(text="Добавить вопрос", callback_data="add_question"))
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="to_admin_panel"))
    return keyboard
