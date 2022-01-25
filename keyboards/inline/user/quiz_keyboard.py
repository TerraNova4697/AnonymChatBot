from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.user.callback_datas import quiz_callback


def create_quiz_keyboard(options):
    keyboard = InlineKeyboardMarkup(row_width=4)
    for num, option in enumerate(options):
        keyboard.insert(InlineKeyboardButton(text=str(num+1), callback_data=quiz_callback
                                             .new(action="quiz_answer", is_true=option[1])))
    keyboard.row(InlineKeyboardButton(text="Отменить", callback_data="cancel"))
    return keyboard
