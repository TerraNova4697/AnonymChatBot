import aiogram.utils.exceptions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from data import variables
from keyboards.inline.cancel_button import cancel_button
from keyboards.inline.user.callback_datas import quiz_callback, forms_callback, forms_importance_callback, \
    important_f_questions_callback, set_value_callback
from keyboards.inline.user.continue_button import begin_search
from keyboards.inline.user.forms_keyboard import create_forms_keyboard
from keyboards.inline.user.important_form_answers_keyboard import create_important_form_answers_keyboard, \
    create_set_value_for_f_questions_keyboard, create_keyboard_to_set_value
from loader import dp, bot, db
from states.fill_in_form import FillInForms


@dp.callback_query_handler(text='fill_in')
async def username_input(call: CallbackQuery):
    await bot.send_message(chat_id=call.message.chat.id, text="Введите Ваше имя", reply_markup=cancel_button)
    await FillInForms.InputUsername.set()


@dp.callback_query_handler(state=FillInForms.InputUsername, text="cancel")
async def cancel_input_username(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=FillInForms.InputUsername)
async def on_username_input(message: types.Message, state: FSMContext):
    db.update_username(user_id=int(message.chat.id), name=message.text)
    await FillInForms.FillInForm.set()
    await state.update_data({"f_questions": variables.f_questions})
    data = await state.get_data()
    f_questions = data.get("f_questions")
    await state.update_data({"num_of_questions": len(f_questions)})
    question = list(f_questions)[0]
    options = f_questions.get(question)
    question += '\n\n'
    question += '\n'.join([
        f'{str(num + 1)}. {option[0]}' for num, option in enumerate(options)
    ])
    keyboard = create_forms_keyboard(options)
    await bot.send_message(chat_id=message.chat.id, text=question, reply_markup=keyboard)


@dp.callback_query_handler(state=FillInForms.FillInForm, text='cancel')
async def on_back_pressed(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.callback_query_handler(forms_callback.filter(action="fill_in_form"), state=FillInForms.FillInForm)
async def on_forms_answer_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
    f_answer_id = callback_data.get("f_ans_id")
    # try:
    #     await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    # except aiogram.utils.exceptions.MessageToDeleteNotFound:
    #     print("Message to delete not found")
    f_answer = db.select_f_answer(answer_id=int(f_answer_id))
    f_question_text = db.select_f_question_form(f_questions_id=int(f_answer[1]))

    try:
        db.update_users_filled_forms_with_answer(user_id=int(call.message.chat.id),
                                                 f_question_id=f_answer[1],
                                                 f_answer_id=int(f_answer_id))

    except Exception as err:
        print(err)

    # Удаляем отвеченный вопрос
    data = await state.get_data()
    questions: dict = data.get("f_questions")
    try:
        questions.pop(f_question_text[1])
    except Exception as err:
        print(err)
    # answered_question = db.select_users_filled_form(user_id=int(call.message.chat.id), f_question_text=f_question_text)
    # q = list(questions)[0]

    # print(q)
    # questions.pop(list(questions)[0])

    # Если вопросы закончились, то завершаем тест
    if len(questions) == 0:
        await state.finish()
        text = "Отлично! Теперь Вы готовы к поиску собеседника."
        await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    reply_markup=begin_search)
    else:
        # Обновляем список вопросов в машине состояний и отправить пользователю новый вопрос
        await state.update_data({"f_questions": questions})
        question = list(questions)[0]
        options = questions.get(question)
        question += '\n\n'
        question += '\n'.join([
            f'{str(num + 1)}. {option[0]}' for num, option in enumerate(options)
        ])
        keyboard = create_forms_keyboard(options)
        await bot.edit_message_text(chat_id=call.message.chat.id, text=question, message_id=call.message.message_id,
                                    reply_markup=keyboard)
        await call.answer()

# @dp.callback_query_handler(forms_importance_callback.filter(action="importance"), state=FillInForms.ChooseImportant)
# async def on_question_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
#     await call.answer()
#     record_id = callback_data.get("record_id")
#     filled_form = db.select_users_filled_form(record_id=int(record_id))
#     print(filled_form)
#     if filled_form[5] == "False":
#         db.users_filled_forms_set_importance(record_id=int(record_id), is_important="True")
#     elif filled_form[5] == "True":
#         db.users_filled_forms_set_importance(record_id=int(record_id), is_important="False")
#     # Достать рекорд_айди и обновить важность вопроса
#     text_begin = "Теперь выберите 3 важные критерия для Вас при поиске " \
#                  "собеседника, кликнув на них по очереди.\n\n" \
#                  "Если Вы хотите убрать какой-то критерий, кликните на него еще раз\n\n"
#     filled_form = db.select_all_users_filled_forms(user_id=call.message.chat.id)
#     text, keyboard = create_important_form_answers_keyboard(filled_form)
#     await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                         reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text="important_done", state=FillInForms.ChooseImportant)
# async def on_important_done_clicked(call: CallbackQuery, state: FSMContext):
#     important_f_questions_count = db.count_all_important_f_questions(user_id=call.message.chat.id, is_important='True')
#     if important_f_questions_count[0][0] != 3:
#         await call.answer(text="Необходимо выбрать 3 критерия", show_alert=True)
#     else:
#         await call.answer()
#         questions = db.select_all_users_filled_forms(is_important="True", user_id=int(call.message.chat.id))
#         text_begin = "Вы выбрали приоритетными следующие критерии: \n\n"
#         text, keyboard = create_set_value_for_f_questions_keyboard(questions)
#         text_end = "\n\nТеперь выберите значение критериев."
#         await bot.edit_message_text(text=text_begin+text+text_end, chat_id=call.message.chat.id,
#                                     message_id=call.message.message_id, reply_markup=keyboard)
#         await FillInForms.ChoosePartnersValue.set()
#
#
# @dp.callback_query_handler(important_f_questions_callback.filter(action="set_value"),
#                            state=FillInForms.ChoosePartnersValue)
# async def on_set_value_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
#     await call.answer()
#     record_id = callback_data.get("record_id")
#     await state.update_data({"current_record": record_id})
#     f_questions_id = callback_data.get("f_questions_id")
#     f_questions = db.select_f_question_form(f_questions_id=int(f_questions_id))
#     text_begin = f"Выберите значение\n\n{f_questions[1]}\n\n"
#     f_answers = db.select_all_f_answers(form_question_id=int(f_questions_id))
#     text, keyboard = create_keyboard_to_set_value(f_answers)
#     await bot.edit_message_text(text=text_begin+text, chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                 reply_markup=keyboard)
#
#
# @dp.callback_query_handler(set_value_callback.filter(action="save_value"), state=FillInForms.ChoosePartnersValue)
# async def on_save_value_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
#     await call.answer()
#     data = await state.get_data()
#     record_id = data.get("current_record")
#     f_answer_id = callback_data.get("f_answer_id")
#     print(record_id)
#     print(f_answer_id)
#     f_answer = db.select_f_answer(answer_id=int(f_answer_id))
#     print(f_answer)
#     db.users_filled_forms_update_partners_value(record_id=int(record_id), partners_value=f_answer[0])
#     questions = db.select_all_users_filled_forms(is_important="True", user_id=int(call.message.chat.id))
#     text_begin = "Вы выбрали приоритетными следующие критерии: \n\n"
#     text, keyboard = create_set_value_for_f_questions_keyboard(questions)
#     text_end = "\n\nТеперь выберите значение критериев."
#     await bot.edit_message_text(text=text_begin + text + text_end, chat_id=call.message.chat.id,
#                                 message_id=call.message.message_id, reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text="nav_back", state=FillInForms.ChoosePartnersValue)
# async def on_back_clicked(call: CallbackQuery):
#     await call.answer()
#     questions = db.select_all_users_filled_forms(is_important="True", user_id=int(call.message.chat.id))
#     text_begin = "Вы выбрали приоритетными следующие критерии: \n\n"
#     text, keyboard = create_set_value_for_f_questions_keyboard(questions)
#     text_end = "\n\nТеперь выберите значение критериев."
#     await bot.edit_message_text(text=text_begin + text + text_end, chat_id=call.message.chat.id,
#                                 message_id=call.message.message_id, reply_markup=keyboard)
#
#
# @dp.callback_query_handler(text="answers_done", state=FillInForms.ChoosePartnersValue)
# async def on_answers_done_clicked(call: CallbackQuery, state: FSMContext):
#     filled_forms = db.select_all_users_filled_forms(user_id=int(call.message.chat.id), is_important="True")
#     for form in filled_forms:
#         if form[6] == "":
#             await call.answer(text="Необходимо дать значение на все вопросы", show_alert=True)
#         else:
#             await state.finish()
#             text = "Отлично! Теперь Вы готовы к поиску собеседника."
#             await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                         reply_markup=begin_search)
