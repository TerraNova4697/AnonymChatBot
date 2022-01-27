from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin.admin_callback_datas import edit_test_callback, edit_options_callback, \
    delete_test_question_callback, change_test_question_callback

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


def create_edit_test_question_keyboard(options):
    keyboard = InlineKeyboardMarkup(row_width=6)
    for num, option in enumerate(options):
        # print(option)
        keyboard.insert(InlineKeyboardButton(text=f"{str(num+1)}", callback_data=edit_options_callback
                                             .new(action="edit_option", option_id=f"{option[0]}")))

    keyboard.row(InlineKeyboardButton(text="Добавить правильный вариант", callback_data="add_correct"))
    keyboard.row(InlineKeyboardButton(text="Добавить неправильный вариант", callback_data="add_incorrect"))
    keyboard.row(InlineKeyboardButton(text="Изменить вопрос", callback_data=change_test_question_callback
                                      .new(action="change_text", question_id=str(options[0][3]))))
    keyboard.row(InlineKeyboardButton(text="Удалить вопрос", callback_data=delete_test_question_callback
                                      .new(action="del_t_quest", question_id=str(options[0][3]))))
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="nav_to_t_quest"))
    return keyboard


