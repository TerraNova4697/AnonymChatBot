from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsOwnerCall, IsAdminCall, IsOwner, IsAdmin
from keyboards.inline.admin.admin_callback_datas import edit_f_question_callback
from keyboards.inline.admin.edit_f_question_keyboard import create_edit_f_question_keyboard
from keyboards.inline.admin.f_question_deletion import f_question_deletion_keyboard
from keyboards.inline.admin.list_of_f_questions_keyboard import create_list_of_forms_questions_keyboard
from keyboards.inline.cancel_button import cancel_button
from loader import bot, dp, db
from states.AddFormQuestion import AddFormQuestion


@dp.callback_query_handler(IsOwnerCall(), text="add_f_question")
@dp.callback_query_handler(IsAdminCall(), text="add_f_question")
async def add_question(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="Введите новый вопрос", reply_markup=cancel_button)
    await AddFormQuestion.InputQuestion.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddFormQuestion.InputQuestion, text="cancel")
@dp.callback_query_handler(IsAdminCall(), state=AddFormQuestion.InputQuestion, text="cancel")
async def cancel_addition(call: CallbackQuery, state: FSMContext):
    await call.answer()
    questions = db.select_all_forms_questions()
    text_begin = "На данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num + 1)}. {question[1]} " for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.send_message(chat_id=call.message.chat.id, text=text_begin + list_of_questions + text_end,
                           reply_markup=create_list_of_forms_questions_keyboard(questions))
    await state.finish()


@dp.message_handler(IsOwner(), state=AddFormQuestion.InputQuestion)
@dp.message_handler(IsAdmin(), state=AddFormQuestion.InputQuestion)
async def edit_f_question(message: types.Message, state: FSMContext):
    db.add_forms_question(text=message.text)
    question = db.select_f_question_form(text=message.text)
    questions_text = f"{question[1]} \n\nВарианты ответов: \n\n"
    f_answers_text = ''
    f_answers = db.select_all_f_answers(form_question_id=int(question[0]))
    if len(f_answers) > 0:
        f_answers_text += "\n".join([
            f"{str(num + 1)}. {answer[0]} " for num, answer in enumerate(f_answers)
        ])
    else:
        f_answers_text = 'Варианты ответов не заданы. Чтобы добавить кликните на кнопку "Добавить варианты ответов"'
    await state.update_data({"f_question_id": question[0]})
    await bot.send_message(chat_id=message.chat.id, text=questions_text + f_answers_text,
                           reply_markup=create_edit_f_question_keyboard(question[0]))
    await AddFormQuestion.QuestionMenu.set()


@dp.callback_query_handler(IsOwnerCall(), state=AddFormQuestion.QuestionMenu, text='to_f_questions')
@dp.callback_query_handler(IsAdminCall(), state=AddFormQuestion.QuestionMenu, text='to_f_questions')
async def navigate_to_form_questions(call: CallbackQuery, state: FSMContext):
    await call.answer()
    questions = db.select_all_forms_questions()
    text_begin = "На данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num + 1)}. {question[1]} " for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.send_message(chat_id=call.message.chat.id, text=text_begin + list_of_questions + text_end,
                           reply_markup=create_list_of_forms_questions_keyboard(questions))
    await state.finish()


@dp.callback_query_handler(IsOwnerCall(), edit_f_question_callback.filter(action="finish"),
                           state=AddFormQuestion.QuestionMenu)
@dp.callback_query_handler(IsAdminCall(), edit_f_question_callback.filter(action="finish"),
                           state=AddFormQuestion.QuestionMenu)
async def finish_forms_question(call: CallbackQuery, state: FSMContext, callback_data: dict):
    # await call.answer()
    f_question_id = callback_data.get("f_question_id")
    f_answers = db.select_all_f_answers(form_question_id=int(f_question_id))
    if len(f_answers) < 2:
        print(len(f_answers))
        # await bot.send_message(chat_id=call.message.chat.id, text="Нужно указать более одного варианта ответа")
        await call.answer(text="Нужно указать более одного варианта ответа", show_alert=True)
    else:
        db.activate_f_question(f_questions_id=int(f_question_id))
        questions = db.select_all_forms_questions()
        text_begin = "На данный момент имеются следующие вопросы: \n\n"
        list_of_questions = ''
        if len(questions) > 0:
            list_of_questions += "\n".join([
                f"{str(num + 1)}. {question[1]} " for num, question in enumerate(questions)
            ])
        else:
            list_of_questions = 'Пока нет вопросов'
        text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
        await bot.send_message(chat_id=call.message.chat.id, text=text_begin + list_of_questions + text_end,
                               reply_markup=create_list_of_forms_questions_keyboard(questions))
        await state.finish()


@dp.callback_query_handler(IsOwnerCall(), edit_f_question_callback.filter(action="add_option"),
                           state=AddFormQuestion.QuestionMenu)
@dp.callback_query_handler(IsAdminCall(), edit_f_question_callback.filter(action="add_option"),
                           state=AddFormQuestion.QuestionMenu)
async def add_option(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(text="Введите новый вариант ответа", chat_id=call.message.chat.id,
                                message_id=call.message.message_id, reply_markup=cancel_button)
    await AddFormQuestion.NewOption.set()


@dp.callback_query_handler(IsOwnerCall(), text="cancel", state=AddFormQuestion.NewOption)
@dp.callback_query_handler(IsAdminCall(), text="cancel", state=AddFormQuestion.NewOption)
async def navigate_to_question_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    f_question_id = data.get("f_question_id")
    question = db.select_f_question_form(f_questions_id=int(f_question_id))
    questions_text = f"{question[1]} \n\nВарианты ответов: \n\n"
    f_answers_text = ''
    f_answers = db.select_all_f_answers(form_question_id=int(question[0]))
    if len(f_answers) > 0:
        f_answers_text += "\n".join([
            f"{str(num + 1)}. {answer[0]} " for num, answer in enumerate(f_answers)
        ])
    else:
        f_answers_text = 'Варианты ответов не заданы. Чтобы добавить кликните на кнопку "Добавить варианты ответов"'
    await state.update_data({"f_question_id": question[0]})
    await bot.send_message(chat_id=call.message.chat.id, text=questions_text + f_answers_text,
                           reply_markup=create_edit_f_question_keyboard(question[0]))
    await AddFormQuestion.QuestionMenu.set()


@dp.message_handler(IsOwner(), state=AddFormQuestion.NewOption)
@dp.message_handler(IsAdmin(), state=AddFormQuestion.NewOption)
async def create_new_option(message: types.Message, state: FSMContext):
    data = await state.get_data()
    f_questions_id = data.get("f_question_id")
    db.insert_new_form_answer(form_question_id=int(f_questions_id), text=message.text)
    question = db.select_f_question_form(f_questions_id=int(f_questions_id))
    questions_text = f"{question[1]} \n\nВарианты ответов: \n\n"
    f_answers_text = ''
    f_answers = db.select_all_f_answers(form_question_id=int(question[0]))
    if len(f_answers) > 0:
        f_answers_text += "\n".join([
            f"{str(num + 1)}. {answer[0]} " for num, answer in enumerate(f_answers)
        ])
    else:
        f_answers_text = 'Варианты ответов не заданы. Чтобы добавить кликните на кнопку "Добавить варианты ответов"'
    await state.update_data({"f_question_id": question[0]})
    await bot.send_message(chat_id=message.chat.id, text=questions_text + f_answers_text,
                           reply_markup=create_edit_f_question_keyboard(question[0]))
    await AddFormQuestion.QuestionMenu.set()


@dp.callback_query_handler(IsOwnerCall(), text="delete_f_question", state=AddFormQuestion.QuestionMenu)
@dp.callback_query_handler(IsAdminCall(), text="delete_f_question", state=AddFormQuestion.QuestionMenu)
async def confirm_deletion(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    f_questions_id = data.get("f_question_id")
    question = db.select_f_question_form(f_questions_id=int(f_questions_id))
    await bot.edit_message_text(text=f"Вы собираетесь удалить вопрос: \n{question[1]}\n\nУверены?",
                                chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=f_question_deletion_keyboard)
    await AddFormQuestion.DeleteQuestion.set()


@dp.callback_query_handler(IsOwnerCall(), text="cancel_deletion", state=AddFormQuestion.DeleteQuestion)
@dp.callback_query_handler(IsAdminCall(), text="cancel_deletion", state=AddFormQuestion.DeleteQuestion)
async def navigate_to_question_edition(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    f_questions_id = data.get("f_question_id")
    question = db.select_f_question_form(f_questions_id=int(f_questions_id))
    questions_text = f"{question[1]} \n\nВарианты ответов: \n\n"
    f_answers_text = ''
    f_answers = db.select_all_f_answers(form_question_id=int(question[0]))
    if len(f_answers) > 0:
        f_answers_text += "\n".join([
            f"{str(num + 1)}. {answer[0]} " for num, answer in enumerate(f_answers)
        ])
    else:
        f_answers_text = 'Варианты ответов не заданы. Чтобы добавить кликните на кнопку "Добавить варианты ответов"'
    await state.update_data({"f_question_id": question[0]})
    await bot.send_message(chat_id=call.message.chat.id, text=questions_text + f_answers_text,
                           reply_markup=create_edit_f_question_keyboard(question[0]))
    await AddFormQuestion.QuestionMenu.set()


@dp.callback_query_handler(IsOwnerCall(), text="confirmed", state=AddFormQuestion.DeleteQuestion)
@dp.callback_query_handler(IsAdminCall(), text="confirmed", state=AddFormQuestion.DeleteQuestion)
async def navigate_to_question_edition(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    f_questions_id = data.get("f_question_id")
    db.delete_f_question(f_questions_id=int(f_questions_id))
    questions = db.select_all_forms_questions()
    text_begin = "Вопрос был удален.\nНа данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num + 1)}. {question[1]} " for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.send_message(chat_id=call.message.chat.id, text=text_begin + list_of_questions + text_end,
                           reply_markup=create_list_of_forms_questions_keyboard(questions))
    await state.finish()
