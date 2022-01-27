from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.variables import test
from keyboards.inline.admin.admin_callback_datas import edit_test_callback


def create_text_and_keyboard():
    list_of_questions = list(test.keys())
    text = "На данный момент существуют следующие вопросы:\n\n"
    for num, question in enumerate(list_of_questions):
        if len(question) > 80:
            text += f"{num + 1}. {question[:60]}...\n"
        else:
            text += f"{num + 1}. {question}\n"

    keyboard = InlineKeyboardMarkup(row_width=6)
    for num, question in enumerate(list_of_questions):
        # print(test[question])
        keyboard.insert(InlineKeyboardButton(text=f"{num + 1}", callback_data=edit_test_callback
                                             .new(action="edit_test", question_id=str(test[question][0][2]))))
    keyboard.row(InlineKeyboardButton(text="Добавить вопрос", callback_data="add_test_question"))
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="test_to_main"))

    return text, keyboard


def create_options_text(options):
    if len(options) == 0:
        return "Пока нет вариантов ответа"
    text = ''
    for num, option in enumerate(options):
        is_true = 'Не верный'
        if option[1] == "True":
            is_true = "Верный"
        text += f"{str(num + 1)}. {option[0]} ({is_true})\n"
    return text


def create_options_text_for_editing(options):
    if len(options) == 0:
        return "Пока нет вариантов ответа"
    text = ''
    for num, option in enumerate(options):
        is_true = 'Не верный'
        if option[2] == "True":
            is_true = "Верный"
        text += f"{str(num + 1)}. {option[1]} ({is_true})\n"
    return text


if __name__ == "__main__":
    create_text_and_keyboard()
