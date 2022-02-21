from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data import variables
from keyboards.inline.user.callback_datas import quiz_callback, forms_importance_callback, \
    important_f_questions_callback, set_value_callback
from keyboards.inline.user.continue_button import continue_button, accept_button, try_again_button, go_on_button, \
    fill_in_button, begin_search
from keyboards.inline.user.important_form_answers_keyboard import create_important_form_answers_keyboard, \
    create_set_value_for_f_questions_keyboard, create_keyboard_to_set_value
from keyboards.inline.user.quiz_keyboard import create_quiz_keyboard
from loader import dp, bot, db
from states.fill_in_form import FillInForms
from states.quiz import QuizState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await bot.send_message(text=f"Привет, {message.from_user.full_name}!", chat_id=message.chat.id,
                           reply_markup=continue_button)
    try:
        db.add_user(int(message.chat.id))
    except Exception as err:
        print(err)


@dp.callback_query_handler(text="continue")
async def new_user_continued(call: CallbackQuery):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text="Текст для ознакомления", reply_markup=accept_button)


@dp.callback_query_handler(text="accept")
async def start_test(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await QuizState.Quiz.set()
    await state.update_data({"questions": variables.test})
    await state.update_data({"points": 0})
    data = await state.get_data("questions")
    questions = data.get("questions")
    await state.update_data({"num_of_questions": len(questions)})
    question = list(questions)[0]
    options = questions.get(question)
    question += '\n\n'
    question += '\n'.join([
        f'{str(num+1)}. {option[0]}' for num, option in enumerate(options)
    ])
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=question,
                                reply_markup=create_quiz_keyboard(options))


@dp.callback_query_handler(text="cancel", state=QuizState.Quiz)
async def cancel_quiz(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text="К сожалению Вы не прошли тестирование. Вы можете в любое время"
                                     " попробовать еще раз", reply_markup=try_again_button)
    await state.finish()


@dp.callback_query_handler(quiz_callback.filter(action="quiz_answer"), state=QuizState.Quiz)
async def check_answer(call: CallbackQuery, state: FSMContext, callback_data: dict):
    # TODO: Удалять сообщение
    await call.answer()
    answer = callback_data.get("is_true")

    # Проверяем правильность ответа и добавляем один балл в случае правильности. Сохраняем в FSMContext
    if answer == "True":
        data = await state.get_data()
        points = data.get("points")
        points += 1
        await state.update_data({"points": points})

    # Удаляем первый (уже отвеченный) вопрос из списка вопросов
    data = await state.get_data("questions")
    questions = data.get("questions")
    questions.pop(list(questions)[0])

    # Если вопросы закончились, то завершаем тест
    if len(questions) == 0:
        data = await state.get_data()
        points = data.get("points")
        num_of_questions = data.get('num_of_questions')
        if points >= num_of_questions-1:
            db.activate_user(user_id=int(call.message.chat.id), status="Active")
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text="Вы успешно прошли тестирование", reply_markup=go_on_button)
        else:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text="К сожалению Вы не прошли тестирование. Вы можете в любое время"
                                             " попробовать еще раз", reply_markup=try_again_button)
        await state.finish()
    else:
        # Обновляем список вопросов в машине состояний и отправить пользователю новый вопрос
        await state.update_data({"questions": questions})
        question = list(questions)[0]
        options = questions.get(question)
        question += '\n\n'
        question += '\n'.join([
            f'{str(num + 1)}. {option[0]}' for num, option in enumerate(options)
        ])
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=question,
                                    reply_markup=create_quiz_keyboard(options))


@dp.callback_query_handler(text="go_on")
async def on_go_on_clicked(call: CallbackQuery):
    text_begin = "Теперь выберите 3 важные критерия для Вас при поиске " \
                 "собеседника, кликнув на них по очереди.\n\n" \
                 "Если Вы хотите убрать какой-то критерий, кликните на него еще раз\n\n"
    f_questions = db.select_all_active_forms_questions()
    for item in f_questions:
        db.insert_users_forms_answers_before_test(user_id=int(call.message.chat.id), f_question_id=item[0],
                                                  f_question_text=item[1])
    unfilled_form = db.select_all_users_filled_forms(user_id=call.message.chat.id)
    text, keyboard = create_important_form_answers_keyboard(unfilled_form)
    await bot.edit_message_text(chat_id=call.message.chat.id, text=text_begin + text,
                                message_id=call.message.message_id,
                                reply_markup=keyboard)
    await FillInForms.ChooseImportant.set()
    await call.answer()


@dp.callback_query_handler(forms_importance_callback.filter(action="importance"), state=FillInForms.ChooseImportant)
async def on_question_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    record_id = callback_data.get("record_id")
    filled_form = db.select_users_filled_form(record_id=int(record_id))
    print(filled_form)
    if filled_form[5] == "False":
        db.users_filled_forms_set_importance(record_id=int(record_id), is_important="True")
    elif filled_form[5] == "True":
        db.users_filled_forms_set_importance(record_id=int(record_id), is_important="False")
    # Достать рекорд_айди и обновить важность вопроса
    text_begin = "Теперь выберите 3 важные критерия для Вас при поиске " \
                 "собеседника, кликнув на них по очереди.\n\n" \
                 "Если Вы хотите убрать какой-то критерий, кликните на него еще раз\n\n"
    filled_form = db.select_all_users_filled_forms(user_id=call.message.chat.id)
    text, keyboard = create_important_form_answers_keyboard(filled_form)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=keyboard)


@dp.callback_query_handler(text="important_done", state=FillInForms.ChooseImportant)
async def on_important_done_clicked(call: CallbackQuery, state: FSMContext):
    important_f_questions_count = db.count_all_important_f_questions(user_id=call.message.chat.id, is_important='True')
    if important_f_questions_count[0][0] != 3:
        await call.answer(text="Необходимо выбрать 3 критерия", show_alert=True)
    else:
        await call.answer()
        questions = db.select_all_users_filled_forms(is_important="True", user_id=int(call.message.chat.id))
        text_begin = "Вы выбрали приоритетными следующие критерии: \n\n"
        text, keyboard = create_set_value_for_f_questions_keyboard(questions)
        text_end = "\n\nТеперь выберите значение критериев."
        await bot.edit_message_text(text=text_begin+text+text_end, chat_id=call.message.chat.id,
                                    message_id=call.message.message_id, reply_markup=keyboard)
        await FillInForms.ChoosePartnersValue.set()


@dp.callback_query_handler(important_f_questions_callback.filter(action="set_value"),
                           state=FillInForms.ChoosePartnersValue)
async def on_set_value_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    record_id = callback_data.get("record_id")
    await state.update_data({"current_record": record_id})
    f_questions_id = callback_data.get("f_questions_id")
    f_questions = db.select_f_question_form(f_questions_id=int(f_questions_id))
    text_begin = f"Выберите значение\n\n{f_questions[1]}\n\n"
    f_answers = db.select_all_f_answers(form_question_id=int(f_questions_id))
    text, keyboard = create_keyboard_to_set_value(f_answers)
    await bot.edit_message_text(text=text_begin+text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                reply_markup=keyboard)


@dp.callback_query_handler(set_value_callback.filter(action="save_value"), state=FillInForms.ChoosePartnersValue)
async def on_save_value_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    data = await state.get_data()
    record_id = data.get("current_record")
    f_answer_id = callback_data.get("f_answer_id")
    print(record_id)
    print(f_answer_id)
    f_answer = db.select_f_answer(answer_id=int(f_answer_id))
    print(f_answer)
    db.users_filled_forms_update_partners_value(record_id=int(record_id), partners_value=f_answer[0])
    questions = db.select_all_users_filled_forms(is_important="True", user_id=int(call.message.chat.id))
    text_begin = "Вы выбрали приоритетными следующие критерии: \n\n"
    text, keyboard = create_set_value_for_f_questions_keyboard(questions)
    text_end = "\n\nТеперь выберите значение критериев."
    await bot.edit_message_text(text=text_begin + text + text_end, chat_id=call.message.chat.id,
                                message_id=call.message.message_id, reply_markup=keyboard)


@dp.callback_query_handler(text="nav_back", state=FillInForms.ChoosePartnersValue)
async def on_back_clicked(call: CallbackQuery):
    await call.answer()
    questions = db.select_all_users_filled_forms(is_important="True", user_id=int(call.message.chat.id))
    text_begin = "Вы выбрали приоритетными следующие критерии: \n\n"
    text, keyboard = create_set_value_for_f_questions_keyboard(questions)
    text_end = "\n\nТеперь выберите значение критериев."
    await bot.edit_message_text(text=text_begin + text + text_end, chat_id=call.message.chat.id,
                                message_id=call.message.message_id, reply_markup=keyboard)


@dp.callback_query_handler(text="answers_done", state=FillInForms.ChoosePartnersValue)
async def on_answers_done_clicked(call: CallbackQuery, state: FSMContext):
    filled_forms = db.select_all_users_filled_forms(user_id=int(call.message.chat.id), is_important="True")
    for form in filled_forms:
        if form[6] == "":
            await call.answer(text="Необходимо дать значение на все вопросы", show_alert=True)
        else:
            await state.finish()
            text = "Отлично! Мы уже нашли подходящего собеседника. Чтобы с ним связаться и понять насколько Вы " \
                   "подходите ему заполните информацию о себе."
            await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        reply_markup=fill_in_button)


# @dp.callback_query_handler(text="go_on")
# async def on_go_on_clicked(call: CallbackQuery):
#     await call.answer()
#     await bot.send_message(chat_id=call.message.chat.id, text="Текст", reply_markup=fill_in_button)
