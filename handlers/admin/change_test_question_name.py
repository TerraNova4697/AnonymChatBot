from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from data import variables
from filters import IsAdminCall, IsOwnerCall, IsOwner, IsAdmin
from keyboards.inline.admin.admin_callback_datas import change_test_question_callback
from keyboards.inline.admin.edit_test_question_keyboard import create_edit_test_question_keyboard
from keyboards.inline.cancel_button import cancel_button
from loader import dp, bot, db
from states.edit_test_question import EditTestQuestion
from utils.prepare_text_keyboard_edit_test import create_options_text_for_editing, create_text_and_keyboard


@dp.callback_query_handler(IsAdminCall(), change_test_question_callback.filter(action="change_text"),
                           state=EditTestQuestion.Edit)
@dp.callback_query_handler(IsOwnerCall(), change_test_question_callback.filter(action="change_text"),
                           state=EditTestQuestion.Edit)
async def on_change_text_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    await state.update_data({"question_id": int(question_id)})
    await bot.send_message(chat_id=call.message.chat.id, text="Введите новое значение", reply_markup=cancel_button)
    await EditTestQuestion.ChangeText.set()


@dp.callback_query_handler(IsAdminCall(), text="cancel", state=EditTestQuestion.ChangeText)
@dp.callback_query_handler(IsOwnerCall(), text="cancel", state=EditTestQuestion.ChangeText)
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


@dp.message_handler(IsAdmin(), state=EditTestQuestion.ChangeText)
@dp.message_handler(IsOwner(), state=EditTestQuestion.ChangeText)
async def on_text_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_id = data.get("question_id")
    old_question_text = db.select_test_question_text(question_id=int(question_id))
    options = variables.test.get(old_question_text[0])
    # print(options)
    variables.test.pop(old_question_text[0])
    variables.test[message.text] = options
    db.update_test_question_text(question_id=int(question_id), question_text=message.text)
    # text, keyboard = create_text_and_keyboard()
    # await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)
    # await state.finish()
    text = db.select_test_question_text(question_id=question_id)
    question_text = text[0]
    options = db.select_all_test_answers(question_id=question_id)
    options_text = create_options_text_for_editing(options)
    keyboard = create_edit_test_question_keyboard(options)
    await bot.send_message(chat_id=message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await EditTestQuestion.Edit.set()
