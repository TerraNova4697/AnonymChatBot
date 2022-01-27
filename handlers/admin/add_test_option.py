from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import variables
from filters import IsAdminCall, IsOwnerCall, IsAdmin, IsOwner
from keyboards.inline.admin.edit_test_question_keyboard import create_edit_test_question_keyboard
from keyboards.inline.cancel_button import cancel_button
from loader import dp, bot, db
from states.edit_test_question import EditTestQuestion
from utils.prepare_text_keyboard_edit_test import create_options_text_for_editing


@dp.callback_query_handler(IsAdminCall(), text="add_correct", state=EditTestQuestion.Edit)
@dp.callback_query_handler(IsOwnerCall(), text="add_correct", state=EditTestQuestion.Edit)
async def on_add_correct_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Введите верный вариант ответа",
                           reply_markup=cancel_button)
    await EditTestQuestion.AddCorrectOption.set()


@dp.callback_query_handler(IsAdminCall(), text="cancel", state=EditTestQuestion.AddCorrectOption)
@dp.callback_query_handler(IsOwnerCall(), text="cancel", state=EditTestQuestion.AddCorrectOption)
async def on_cancel_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    question_id = data.get("question_id")
    text = db.select_test_question_text(question_id=question_id)
    question_text = text[0]
    options = db.select_all_test_answers(question_id=question_id)
    options_text = create_options_text_for_editing(options)
    keyboard = create_edit_test_question_keyboard(options)
    await bot.send_message(chat_id=call.message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await EditTestQuestion.Edit.set()
    await state.update_data({"question_id": int(question_id)})


@dp.message_handler(IsAdmin(), state=EditTestQuestion.AddCorrectOption)
@dp.message_handler(IsOwner(), state=EditTestQuestion.AddCorrectOption)
async def on_correct_option_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_id = data.get("question_id")
    db.add_test_option(answer_text=message.text, is_true="True", question_id=int(question_id))
    list_of_test_questions = db.select_all_test_questions()
    for question in list_of_test_questions:
        list_of_answers = db.select_test_answers(question_id=question[0])
        variables.test[question[1]] = list_of_answers
    text = db.select_test_question_text(question_id=question_id)
    question_text = text[0]
    options = db.select_all_test_answers(question_id=question_id)
    options_text = create_options_text_for_editing(options)
    keyboard = create_edit_test_question_keyboard(options)
    await bot.send_message(chat_id=message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await EditTestQuestion.Edit.set()
    await state.update_data({"question_id": int(question_id)})


@dp.callback_query_handler(IsAdminCall(), text="add_incorrect", state=EditTestQuestion.Edit)
@dp.callback_query_handler(IsOwnerCall(), text="add_incorrect", state=EditTestQuestion.Edit)
async def on_add_correct_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Введите неверный вариант ответа",
                           reply_markup=cancel_button)
    await EditTestQuestion.AddIncorrectOption.set()


@dp.callback_query_handler(IsAdminCall(), text="cancel", state=EditTestQuestion.AddIncorrectOption)
@dp.callback_query_handler(IsOwnerCall(), text="cancel", state=EditTestQuestion.AddIncorrectOption)
async def on_cancel_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    question_id = data.get("question_id")
    text = db.select_test_question_text(question_id=question_id)
    question_text = text[0]
    options = db.select_all_test_answers(question_id=question_id)
    options_text = create_options_text_for_editing(options)
    keyboard = create_edit_test_question_keyboard(options)
    await bot.send_message(chat_id=call.message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await EditTestQuestion.Edit.set()
    await state.update_data({"question_id": int(question_id)})


@dp.message_handler(IsAdmin(), state=EditTestQuestion.AddIncorrectOption)
@dp.message_handler(IsOwner(), state=EditTestQuestion.AddIncorrectOption)
async def on_correct_option_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_id = data.get("question_id")
    db.add_test_option(answer_text=message.text, is_true="False", question_id=int(question_id))
    list_of_test_questions = db.select_all_test_questions()
    for question in list_of_test_questions:
        list_of_answers = db.select_test_answers(question_id=question[0])
        variables.test[question[1]] = list_of_answers
    text = db.select_test_question_text(question_id=question_id)
    question_text = text[0]
    options = db.select_all_test_answers(question_id=question_id)
    options_text = create_options_text_for_editing(options)
    keyboard = create_edit_test_question_keyboard(options)
    await bot.send_message(chat_id=message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await EditTestQuestion.Edit.set()
    await state.update_data({"question_id": int(question_id)})
