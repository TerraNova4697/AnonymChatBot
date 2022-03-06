from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import variables
from filters import IsOwnerCall, IsAdminCall, IsOwner, IsAdmin
from keyboards.inline.admin.admin_callback_datas import choose_openness_callback, edit_category_keyboard
from keyboards.inline.admin.choose_opennes_keyboard import choose_openness_keyboard
from keyboards.inline.admin.edit_category_keyboard import create_edit_category_keyboard
from keyboards.inline.admin.input_quest_category import input_category_keyboard
from keyboards.inline.admin.list_of_questions_keyboard import create_list_of_questions_keyboard
from keyboards.inline.cancel_button import cancel_button
from loader import dp, bot, db
from states.add_question import AddQuestion


@dp.callback_query_handler(IsOwnerCall(), text="add_question")
@dp.callback_query_handler(IsAdminCall(), text="add_question")
async def add_question(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Введите новый вопрос", reply_markup=cancel_button)
    await AddQuestion.InputQuestion.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddQuestion.InputQuestion, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=AddQuestion.InputQuestion, text="cancel")
async def cancel_addition(call: CallbackQuery, state: FSMContext):
    await call.answer()
    questions = db.select_all_questions()
    text_begin = "На данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num + 1)}. {question[1]} ({question[2]})" for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.send_message(chat_id=call.message.chat.id, text=text_begin + list_of_questions + text_end,
                           reply_markup=create_list_of_questions_keyboard(questions))
    await state.finish()


@dp.message_handler(IsOwner(), state=AddQuestion.InputQuestion)
@dp.message_handler(IsAdmin(), state=AddQuestion.InputQuestion)
async def choose_openness(message: types.Message, state: FSMContext):
    await state.update_data({"question": message.text})
    await bot.send_message(chat_id=message.chat.id, text="Выберите уровень откровенности",
                           reply_markup=choose_openness_keyboard)
    await AddQuestion.InputOpenness.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddQuestion.InputOpenness, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=AddQuestion.InputOpenness, text="cancel")
async def navigate_to_admin_panel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    questions = db.select_all_questions()
    text_begin = "На данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num + 1)}. {question[1]} ({question[2]})" for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.send_message(chat_id=call.message.chat.id, text=text_begin + list_of_questions + text_end,
                           reply_markup=create_list_of_questions_keyboard(questions))
    await state.finish()


@dp.callback_query_handler(IsOwnerCall(), choose_openness_callback.filter(action="openness"),
                           state=AddQuestion.InputOpenness)
@dp.callback_query_handler(IsAdminCall(), choose_openness_callback.filter(action="openness"),
                           state=AddQuestion.InputOpenness)
async def input_category(call: CallbackQuery, state: FSMContext, callback_data: dict):
    openness = callback_data.get("openness")
    await state.update_data({"openness": openness})
    await bot.send_message(chat_id=call.message.chat.id,
                           text="Введите новое значение вручную или выберите из существующих",
                           reply_markup=create_edit_category_keyboard())
    await AddQuestion.InputCategory.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddQuestion.InputCategory, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=AddQuestion.InputCategory, text="cancel")
async def navigate_to_admin_panel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    questions = db.select_all_questions()
    text_begin = "На данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num + 1)}. {question[1]} ({question[2]})" for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.send_message(chat_id=call.message.chat.id, text=text_begin + list_of_questions + text_end,
                           reply_markup=create_list_of_questions_keyboard(questions))
    await state.finish()


@dp.callback_query_handler(IsOwnerCall(), edit_category_keyboard.filter(action="edit_cat"),
                           state=AddQuestion.InputCategory)
@dp.callback_query_handler(IsAdminCall(), edit_category_keyboard.filter(action="edit_cat"),
                           state=AddQuestion.InputCategory)
async def add_question_no_category(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    data = await state.get_data()
    question = data.get("question")
    openness = data.get("openness")
    category = callback_data.get("category")
    db.add_question(question=question, category=category, openness=openness)
    new_question = db.select_question(question=question, category=category, openness=openness)
    if question[3] == "Формальный":
        variables.formal_questions.append(new_question)
    elif question[3] == "Приятельский":
        variables.fellowish_questions.append(new_question)
    elif question[3] == "Дружеский":
        variables.friendly_questions.append(new_question)
    elif question[3] == "Близость":
        variables.close_friend_questions.append(new_question)
    elif question[3] == "Исповедь":
        variables.confession_questions.append(new_question)
    questions = db.select_all_questions()
    text_begin = "Вы добавили новый вопрос. \n\nНа данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num + 1)}. {question[1]} ({question[2]})" for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.send_message(chat_id=call.message.chat.id, text=text_begin + list_of_questions + text_end,
                           reply_markup=create_list_of_questions_keyboard(questions))
    await state.finish()


@dp.message_handler(IsOwner(), state=AddQuestion.InputCategory)
@dp.message_handler(IsAdmin(), state=AddQuestion.InputCategory)
async def add_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question = data.get("question")
    openness = data.get("openness")
    db.add_question(question=question, category=message.text, openness=openness)
    questions = db.select_all_questions()
    text_begin = "Вы добавили новый вопрос. \n\nНа данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num + 1)}. {question[1]} ({question[2]})" for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.send_message(chat_id=message.chat.id, text=text_begin + list_of_questions + text_end,
                           reply_markup=create_list_of_questions_keyboard(questions))
    await state.finish()

