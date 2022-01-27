from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from data import variables
from filters import IsAdminCall, IsOwnerCall, IsOwner, IsAdmin
from keyboards.inline.admin.admin_callback_datas import edit_options_callback
from keyboards.inline.admin.edit_test_question_keyboard import create_edit_test_question_keyboard
from keyboards.inline.cancel_button import cancel_button
from loader import dp, db, bot
from states.edit_test_question import EditTestQuestion
from utils.prepare_text_keyboard_edit_test import create_options_text_for_editing


@dp.callback_query_handler(IsAdminCall(), edit_options_callback.filter(action="edit_option"),
                           state=EditTestQuestion.Edit)
@dp.callback_query_handler(IsOwnerCall(), edit_options_callback.filter(action="edit_option"),
                           state=EditTestQuestion.Edit)
async def on_edit_option_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    option_id = callback_data.get("option_id")
    option = db.select_test_answers(answer_id=int(option_id))
    await state.update_data({"option_id": option_id})
    is_true = "Не верный"
    if option[0][1] == "True":
        is_true = "Верный"
    keyboard = InlineKeyboardMarkup(inline_keyboard=
                                    [
                                        [
                                            InlineKeyboardButton(text="Изменить текст", callback_data="edit_text")
                                        ],
                                        [
                                            InlineKeyboardButton(text="Удалить вариант", callback_data="delete_text")
                                        ],
                                        [
                                            InlineKeyboardButton(text="Назад", callback_data="nav_to_quest")
                                        ]
                                    ])
    await bot.send_message(chat_id=call.message.chat.id, text=f"{option[0][0]} ({is_true})", reply_markup=keyboard)
    await EditTestQuestion.EditOption.set()


@dp.callback_query_handler(IsAdminCall(), text="edit_text", state=EditTestQuestion.EditOption)
@dp.callback_query_handler(IsOwnerCall(), text="edit_text", state=EditTestQuestion.EditOption)
async def on_edit_text_clicked(call: CallbackQuery):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Введите новое значение", reply_markup=cancel_button)
    await EditTestQuestion.NewOptionInput.set()


@dp.callback_query_handler(IsAdminCall(), text="cancel", state=EditTestQuestion.NewOptionInput)
@dp.callback_query_handler(IsOwnerCall(), text="cancel", state=EditTestQuestion.NewOptionInput)
async def on_cancel_pressed(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    option_id = data.get("option_id")
    option = db.select_test_answers(answer_id=int(option_id))
    await state.update_data({"option_id": option_id})
    is_true = "Не верный"
    if option[0][1] == "True":
        is_true = "Верный"
    keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Изменить текст", callback_data="edit_text")
        ],
        [
            InlineKeyboardButton(text="Удалить вариант", callback_data="delete_text")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="nav_to_quest")
        ]
    ])
    await bot.send_message(chat_id=call.message.chat.id, text=f"{option[0][0]} ({is_true})", reply_markup=keyboard)
    await EditTestQuestion.EditOption.set()


@dp.message_handler(IsAdmin(), state=EditTestQuestion.NewOptionInput)
@dp.message_handler(IsOwner(), state=EditTestQuestion.NewOptionInput)
async def on_new_value_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    option_id = data.get("option_id")
    db.update_options_text(answer_id=int(option_id), answer_text=message.text)
    list_of_test_questions = db.select_all_test_questions()
    for question in list_of_test_questions:
        list_of_answers = db.select_test_answers(question_id=question[0])
        variables.test[question[1]] = list_of_answers
    option = db.select_test_answers(answer_id=int(option_id))
    await state.update_data({"option_id": option_id})
    is_true = "Не верный"
    if option[0][1] == "True":
        is_true = "Верный"
    keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Изменить текст", callback_data="edit_text")
        ],
        [
            InlineKeyboardButton(text="Удалить вариант", callback_data="delete_text")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="nav_to_quest")
        ]
    ])
    await bot.send_message(chat_id=message.chat.id, text=f"{option[0][0]} ({is_true})", reply_markup=keyboard)
    await EditTestQuestion.EditOption.set()


@dp.callback_query_handler(IsAdminCall(), text="nav_to_quest", state=EditTestQuestion.EditOption)
@dp.callback_query_handler(IsOwnerCall(), text="nav_to_quest", state=EditTestQuestion.EditOption)
async def on_back_pressed(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    question_id = data.get("question_id")
    text = db.select_test_question_text(question_id=int(question_id))
    question_text = text[0]
    options = db.select_all_test_answers(question_id=int(question_id))
    options_text = create_options_text_for_editing(options)
    keyboard = create_edit_test_question_keyboard(options)
    await bot.send_message(chat_id=call.message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await EditTestQuestion.Edit.set()


@dp.callback_query_handler(IsAdminCall(), text="delete_text", state=EditTestQuestion.EditOption)
@dp.callback_query_handler(IsOwnerCall(), text="delete_text", state=EditTestQuestion.EditOption)
async def on_delete_pressed(call: CallbackQuery, state: FSMContext):
    await call.answer()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить", callback_data="delete")
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel")
        ]
    ])
    await bot.send_message(chat_id=call.message.chat.id, text="Вы уверены, что хотите удалить?", reply_markup=keyboard)
    await EditTestQuestion.DeleteOption.set()


@dp.callback_query_handler(IsAdminCall(), text="cancel", state=EditTestQuestion.DeleteOption)
@dp.callback_query_handler(IsOwnerCall(), text="cancel", state=EditTestQuestion.DeleteOption)
async def on_cancel_pressed(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    option_id = data.get("option_id")
    option = db.select_test_answers(answer_id=int(option_id))
    await state.update_data({"option_id": option_id})
    is_true = "Не верный"
    if option[0][1] == "True":
        is_true = "Верный"
    keyboard = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Изменить текст", callback_data="edit_text")
        ],
        [
            InlineKeyboardButton(text="Удалить вариант", callback_data="delete_text")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="nav_to_quest")
        ]
    ])
    await bot.send_message(chat_id=call.message.chat.id, text=f"{option[0][0]} ({is_true})", reply_markup=keyboard)
    await EditTestQuestion.EditOption.set()


@dp.callback_query_handler(IsAdminCall(), text="delete", state=EditTestQuestion.DeleteOption)
@dp.callback_query_handler(IsOwnerCall(), text="delete", state=EditTestQuestion.DeleteOption)
async def delete_option(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    option_id = data.get("option_id")
    db.delete_option(answer_id=int(option_id))
    list_of_test_questions = db.select_all_test_questions()
    for question in list_of_test_questions:
        list_of_answers = db.select_test_answers(question_id=question[0])
        variables.test[question[1]] = list_of_answers
    question_id = data.get("question_id")
    text = db.select_test_question_text(question_id=int(question_id))
    question_text = text[0]
    options = db.select_all_test_answers(question_id=int(question_id))
    options_text = create_options_text_for_editing(options)
    keyboard = create_edit_test_question_keyboard(options)
    await bot.send_message(chat_id=call.message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await EditTestQuestion.Edit.set()

