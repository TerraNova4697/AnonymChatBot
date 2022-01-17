from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsOwnerCall, IsAdminCall, IsOwner, IsAdmin
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
async def input_category(message: types.Message, state: FSMContext):
    await state.update_data({"question": message.text})
    await bot.send_message(chat_id=message.chat.id, text="Введите категорию вопроса",
                           reply_markup=input_category_keyboard)
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


@dp.callback_query_handler(IsOwnerCall(), state=AddQuestion.InputCategory, text="no_category")
@dp.callback_query_handler(IsAdminCall(), state=AddQuestion.InputCategory, text="no_category")
async def add_question_no_category(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    question = data.get("question")
    db.add_question(question=question, category='Без категории')
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
    db.add_question(question=question, category=message.text)
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

