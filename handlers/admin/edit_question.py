from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsOwnerCall, IsAdminCall, IsOwner, IsAdmin
from keyboards.inline.admin.admin_callback_datas import choose_question_callback, edit_question_keyboard, \
    edit_category_keyboard, delete_question_callback, choose_openness_callback
from keyboards.inline.admin.choose_opennes_keyboard import choose_openness_keyboard
from keyboards.inline.admin.edit_category_keyboard import create_edit_category_keyboard
from keyboards.inline.admin.edit_question_keyboard import create_edit_question_keyboard
from keyboards.inline.admin.list_of_questions_keyboard import create_list_of_questions_keyboard
from keyboards.inline.admin.question_deletion import create_question_deletion_keyboard
from keyboards.inline.cancel_button import cancel_button
from loader import dp, bot, db
from states.edit_question import EditQuestion


@dp.callback_query_handler(IsOwnerCall(), choose_question_callback.filter(action="choose_quest"))
@dp.callback_query_handler(IsAdminCall(), choose_question_callback.filter(action="choose_quest"))
async def send_question_menu(call: CallbackQuery(), callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    question = db.select_question(question_id=int(question_id))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{question[1]}\n\nКатегория: {question[2]}\n\nУровень откровенности: {question[3]}",
                                reply_markup=create_edit_question_keyboard(int(question_id)))


@dp.callback_query_handler(IsOwnerCall(), text="to_questions")
@dp.callback_query_handler(IsAdminCall(), text="to_questions")
async def navigate_to_questions_list(call: CallbackQuery):
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
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text_begin + list_of_questions + text_end,
                                reply_markup=create_list_of_questions_keyboard(questions))


@dp.callback_query_handler(IsOwnerCall(), edit_question_keyboard.filter(action="edit_question"))
@dp.callback_query_handler(IsAdminCall(), edit_question_keyboard.filter(action="edit_question"))
async def input_new_text(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    await state.update_data({"question_id": question_id})
    await bot.edit_message_text(text="Введите новое значение", chat_id=call.message.chat.id,
                                message_id=call.message.message_id, reply_markup=cancel_button)
    await EditQuestion.EditText.set()


@dp.callback_query_handler(IsOwnerCall(), state=EditQuestion.EditText, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=EditQuestion.EditText, text="cancel")
async def cancel_input(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    question_id = data.get("question_id")
    question = db.select_question(question_id=int(question_id))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{question[1]}\n\nКатегория: {question[2]}\n\nУровень откровенности: {question[3]}",
                                reply_markup=create_edit_question_keyboard(int(question_id)))
    await state.finish()


@dp.message_handler(IsOwner(), state=EditQuestion.EditText)
@dp.message_handler(IsAdmin(), state=EditQuestion.EditText)
async def update_questions_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_id = data.get("question_id")
    db.update_questions_text(question_id=int(question_id), question=message.text)
    question = db.select_question(question_id=int(question_id))
    await bot.send_message(chat_id=message.chat.id, text=f"Обновлен: \n{question[1]} ({question[2]})"
                                                         f"\n\nКатегория: {question[2]}\n\nУровень откровенности: {question[3]}",
                           reply_markup=create_edit_question_keyboard(int(question_id)))
    await state.finish()


@dp.callback_query_handler(IsOwnerCall(), edit_question_keyboard.filter(action="edit_cat"))
@dp.callback_query_handler(IsAdminCall(), edit_question_keyboard.filter(action="edit_cat"))
async def input_new_category(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    await state.update_data({"question_id": question_id})
    await bot.edit_message_text(text="Введите новое значение вручную или выберите из существующих",
                                chat_id=call.message.chat.id,
                                message_id=call.message.message_id, reply_markup=create_edit_category_keyboard())
    await EditQuestion.EditCategory.set()


@dp.callback_query_handler(IsOwnerCall(), state=EditQuestion.EditCategory, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=EditQuestion.EditCategory, text="cancel")
async def cancel_input(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    question_id = data.get("question_id")
    question = db.select_question(question_id=int(question_id))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{question[1]}\n\nКатегория: {question[2]}\n\nУровень откровенности: {question[3]}",
                                reply_markup=create_edit_question_keyboard(int(question_id)))
    await state.finish()


@dp.callback_query_handler(IsOwnerCall(), edit_category_keyboard.filter(action="edit_cat"),
                           state=EditQuestion.EditCategory)
@dp.callback_query_handler(IsAdminCall(), edit_category_keyboard.filter(action="edit_cat"),
                           state=EditQuestion.EditCategory)
async def update_category(call: CallbackQuery, state: FSMContext, callback_data: dict):
    new_category = callback_data.get("category")
    data = await state.get_data()
    question_id = data.get("question_id")
    db.update_questions_category(category=new_category, question_id=int(question_id))
    question = db.select_question(question_id=int(question_id))
    await bot.send_message(chat_id=call.message.chat.id, text=f"Обновлен: \n{question[1]} ({question[2]})"
                                                              f"\n\nКатегория: {question[2]}\n\nУровень откровенности: {question[3]}",
                           reply_markup=create_edit_question_keyboard(int(question_id)))
    await state.finish()


@dp.callback_query_handler(IsOwnerCall(), edit_question_keyboard.filter(action="edit_open"))
@dp.callback_query_handler(IsAdminCall(), edit_question_keyboard.filter(action="edit_open"))
async def edit_openness(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    await state.update_data({"question_id": question_id})
    await bot.send_message(chat_id=call.message.chat.id, text="Выберите уровень откровенности",
                           reply_markup=choose_openness_keyboard)
    await EditQuestion.EditOpenness.set()


@dp.callback_query_handler(IsOwnerCall(), state=EditQuestion.EditOpenness, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=EditQuestion.EditOpenness, text="cancel")
async def cancel_input(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    question_id = data.get("question_id")
    question = db.select_question(question_id=int(question_id))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{question[1]}\n\nКатегория: {question[2]}\n\nУровень откровенности: {question[3]}",
                                reply_markup=create_edit_question_keyboard(int(question_id)))
    await state.finish()


@dp.callback_query_handler(IsOwnerCall(), choose_openness_callback.filter(action="openness"),
                           state=EditQuestion.EditOpenness)
@dp.callback_query_handler(IsAdminCall(), choose_openness_callback.filter(action="openness"),
                           state=EditQuestion.EditOpenness)
async def update_openness(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    data = await state.get_data()
    question_id = data.get("question_id")
    openness = callback_data.get("openness")
    db.update_questions_openness(question_id=int(question_id), openness=openness)
    question = db.select_question(question_id=int(question_id))
    await bot.send_message(chat_id=call.message.chat.id, text=f"Обновлен: \n{question[1]} ({question[2]})"
                                                              f"\n\nКатегория: {question[2]}\n\nУровень откровенности: {question[3]}",
                           reply_markup=create_edit_question_keyboard(int(question_id)))
    await state.finish()


@dp.message_handler(IsOwner(), state=EditQuestion.EditCategory)
@dp.message_handler(IsAdmin(), state=EditQuestion.EditCategory)
async def update_category(message: types.Message, state: FSMContext):
    data = await state.get_data()
    question_id = data.get("question_id")
    db.update_questions_category(category=message.text, question_id=int(question_id))
    question = db.select_question(question_id=int(question_id))
    await bot.send_message(chat_id=message.chat.id, text=f"Обновлен: \n{question[1]} ({question[2]})"
                                                         f"\n\nКатегория: {question[2]}\n\nУрвоень откровенности: {question[3]}",
                           reply_markup=create_edit_question_keyboard(int(question_id)))
    await state.finish()


@dp.callback_query_handler(IsOwnerCall(), edit_question_keyboard.filter(action="delete"))
@dp.callback_query_handler(IsAdminCall(), edit_question_keyboard.filter(action="delete"))
async def confirm_deletion(call: CallbackQuery(), state: FSMContext, callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    question = db.select_question(question_id=int(question_id))
    print(question)
    await bot.edit_message_text(text=f"Вы собираетесь удалить вопрос: \n\n{question[1]}\n\nУверены?",
                                reply_markup=create_question_deletion_keyboard(int(question_id)),
                                chat_id=call.message.chat.id, message_id=call.message.message_id)
    await EditQuestion.DeleteQuestion.set()


@dp.callback_query_handler(IsOwnerCall(), delete_question_callback.filter(action="cancel"),
                           state=EditQuestion.DeleteQuestion)
@dp.callback_query_handler(IsAdminCall(), delete_question_callback.filter(action="cancel"),
                           state=EditQuestion.DeleteQuestion)
async def cancel_deletion(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    question_id = callback_data.get("question_id")
    question = db.select_question(question_id=int(question_id))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{question[1]}\n\nКатегория: {question[2]}\n\nУровень откровенности: {question[3]}",
                                reply_markup=create_edit_question_keyboard(int(question_id)))
    await state.finish()


@dp.callback_query_handler(IsOwnerCall(), delete_question_callback.filter(action="delete"),
                           state=EditQuestion.DeleteQuestion)
@dp.callback_query_handler(IsAdminCall(), delete_question_callback.filter(action="delete"),
                           state=EditQuestion.DeleteQuestion)
async def delete_question(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    db.delete_question(question_id=int(question_id))
    questions = db.select_all_questions()
    text_begin = "Вопрос был удален. \nНа данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num + 1)}. {question[1]} ({question[2]})" for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=text_begin + list_of_questions + text_end,
                                reply_markup=create_list_of_questions_keyboard(questions))
    await state.finish()
