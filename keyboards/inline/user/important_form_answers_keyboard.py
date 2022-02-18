from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.user.callback_datas import forms_importance_callback, important_f_questions_callback, \
    set_value_callback


def create_important_form_answers_keyboard(filled_form):
    keyboard = InlineKeyboardMarkup(row_width=5)
    text = ''
    text += "\n".join([
        f"{num + 1}. {answer[3]}" for num, answer in enumerate(filled_form)
    ])
    for num, answer in enumerate(filled_form):
        if answer[5] == "True":
            keyboard.insert(InlineKeyboardButton(text="☑️", callback_data=forms_importance_callback
                                                 .new(action="importance", record_id=answer[0])))
        else:
            keyboard.insert(InlineKeyboardButton(text=str(num + 1), callback_data=forms_importance_callback
                                                 .new(action="importance", record_id=answer[0])))
    keyboard.row(InlineKeyboardButton(text="Готово", callback_data="important_done"))
    return text, keyboard


def create_set_value_for_f_questions_keyboard(questions):
    keyboard = InlineKeyboardMarkup(row_width=5)
    text = ''
    text += "\n".join([
        f"{num + 1}. {question[3]}" for num, question in enumerate(questions)
    ])
    for num, question in enumerate(questions):
        keyboard.insert(InlineKeyboardButton(text=str(num + 1), callback_data=important_f_questions_callback
                                             .new(action="set_value", f_questions_id=question[2], record_id=question[0])))
    keyboard.row(InlineKeyboardButton(text="Готово", callback_data="answers_done"))
    return text, keyboard


def create_keyboard_to_set_value(f_answers):
    keyboard = InlineKeyboardMarkup(row_width=5)
    text = ''
    text += "\n".join([
        f"{num + 1}. {answer[0]}" for num, answer in enumerate(f_answers)
    ])
    for num, answer in enumerate(f_answers):
        keyboard.insert(InlineKeyboardButton(text=str(num + 1), callback_data=set_value_callback
                                             .new(action="save_value", f_answer_id=answer[1])))
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="nav_back"))
    return text, keyboard
