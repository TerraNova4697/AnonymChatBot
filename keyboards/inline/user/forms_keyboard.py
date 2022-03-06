from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.user.callback_datas import forms_callback


def create_forms_keyboard(options):
    keyboard = InlineKeyboardMarkup(row_width=4)
    for num, option in enumerate(options):
        keyboard.insert(InlineKeyboardButton(text=str(num+1), callback_data=forms_callback
                                             .new(action="fill_in_form", f_ans_id=str(option[1]))))
    keyboard.row(InlineKeyboardButton(text="Отменить", callback_data="cancel"))
    return keyboard


def create_forms_update_keyboard(options):
    keyboard = InlineKeyboardMarkup(row_width=4)
    for num, option in enumerate(options):
        keyboard.insert(InlineKeyboardButton(text=str(num+1), callback_data=forms_callback
                                             .new(action="fill_in_form", f_ans_id=str(option[1]))))
    return keyboard
