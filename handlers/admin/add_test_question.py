from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import variables
from data.variables import new_options
from filters import IsOwnerCall, IsAdminCall, IsAdmin, IsOwner
from keyboards.inline.admin.edit_test_question_keyboard import edit_test_question_keyboard
from keyboards.inline.cancel_button import cancel_button
from loader import dp, bot, db
from states.add_new_test_question import AddNewQuestion
from utils.prepare_text_keyboard_edit_test import create_text_and_keyboard, create_options_text


@dp.callback_query_handler(IsOwnerCall(), text="add_test_question")
@dp.callback_query_handler(IsAdminCall(), text="add_test_question")
async def on_add_new_test_question_clicked(call: CallbackQuery):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Введите новый вопрос", reply_markup=cancel_button)
    await AddNewQuestion.NewTestQuestionInput.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddNewQuestion.NewTestQuestionInput, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=AddNewQuestion.NewTestQuestionInput, text="cancel")
async def on_cancel_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    text, keyboard = create_text_and_keyboard()
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard)
    await state.finish()


@dp.message_handler(IsOwner(), state=AddNewQuestion.NewTestQuestionInput)
@dp.message_handler(IsAdmin(), state=AddNewQuestion.NewTestQuestionInput)
async def on_question_input(message: types.Message, state: FSMContext):
    db.add_question_into_test_questions(question_text=message.text)
    question_id = db.select_test_question_id(question_text=message.text)
    await state.update_data({"new_test_question_id": question_id[0]})
    # TODO: Добавить варианты ответа
    options = db.select_test_answers(question_id=question_id[0])
    options_text = create_options_text(options)
    await bot.send_message(chat_id=message.chat.id, text=f"{message.text}\n\nВарианты ответа:\n\n{options_text}",
                           reply_markup=edit_test_question_keyboard)
    await AddNewQuestion.EditTestQuestion.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddNewQuestion.EditTestQuestion, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=AddNewQuestion.EditTestQuestion, text="cancel")
async def on_cancel_clicked(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_test_question_id = data.get("new_test_question_id")
    await call.answer()
    text, keyboard = create_text_and_keyboard()
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard)
    await state.finish()
    db.delete_question_option(question_id=new_test_question_id)


@dp.callback_query_handler(IsOwnerCall(), state=AddNewQuestion.EditTestQuestion, text="add_correct")
@dp.callback_query_handler(IsAdminCall(), state=AddNewQuestion.EditTestQuestion, text="add_correct")
async def on_add_correct_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Введите вариант ответа", reply_markup=cancel_button)
    await AddNewQuestion.AddCorrect.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddNewQuestion.AddCorrect, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=AddNewQuestion.AddCorrect, text="cancel")
async def on_cancel_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    question_id = data.get("new_test_question_id")
    question_text = db.select_test_question_text(question_id=int(question_id))
    await bot.send_message(chat_id=call.message.chat.id, text=f"{question_text[0]}\n\n",
                           reply_markup=edit_test_question_keyboard)
    await AddNewQuestion.EditTestQuestion.set()


@dp.message_handler(IsOwner(), state=AddNewQuestion.AddCorrect)
@dp.message_handler(IsAdmin(), state=AddNewQuestion.AddCorrect)
async def on_new_question_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_test_question_id = data.get("new_test_question_id")
    db.add_test_option(answer_text=message.text, is_true="True", question_id=int(new_test_question_id))
    text = db.select_test_question_text(question_id=new_test_question_id)
    question_text = text[0]
    options = db.select_test_answers(question_id=new_test_question_id)
    options_text = create_options_text(options)
    keyboard = edit_test_question_keyboard
    await bot.send_message(chat_id=message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await AddNewQuestion.EditTestQuestion.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddNewQuestion.EditTestQuestion, text="add_incorrect")
@dp.callback_query_handler(IsAdminCall(), state=AddNewQuestion.EditTestQuestion, text="add_incorrect")
async def on_add_incorrect_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Введите вариант ответа", reply_markup=cancel_button)
    await AddNewQuestion.AddIncorrect.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddNewQuestion.AddIncorrect, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=AddNewQuestion.AddIncorrect, text="cancel")
async def on_cancel_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    question_id = data.get("new_test_question_id")
    question_text = db.select_test_question_text(question_id=int(question_id))
    await bot.send_message(chat_id=call.message.chat.id, text=f"{question_text[0]}\n\n",
                           reply_markup=edit_test_question_keyboard)
    await AddNewQuestion.EditTestQuestion.set()


@dp.message_handler(IsOwner(), state=AddNewQuestion.AddIncorrect)
@dp.message_handler(IsAdmin(), state=AddNewQuestion.AddIncorrect)
async def on_new_question_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    new_test_question_id = data.get("new_test_question_id")
    db.add_test_option(answer_text=message.text, is_true="False", question_id=int(new_test_question_id))
    text = db.select_test_question_text(question_id=new_test_question_id)
    question_text = text[0]
    options = db.select_test_answers(question_id=new_test_question_id)
    options_text = create_options_text(options)
    keyboard = edit_test_question_keyboard
    await bot.send_message(chat_id=message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await AddNewQuestion.EditTestQuestion.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddNewQuestion.EditTestQuestion, text="finish")
@dp.callback_query_handler(IsAdminCall(), state=AddNewQuestion.EditTestQuestion, text="finish")
async def on_finish_clicked(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_test_question_id = data.get("new_test_question_id")
    options = db.select_test_answers(question_id=new_test_question_id)
    if len(options) < 2:
        await call.answer(text="Должно быть минимум два варианта ответа", show_alert=True)
    else:
        db.activate_test_question(question_id=new_test_question_id)
        text, keyboard = create_text_and_keyboard()
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard)
        question_text = db.select_test_question_text(question_id=new_test_question_id)
        variables.test[question_text[1]] = options
        await state.finish()


