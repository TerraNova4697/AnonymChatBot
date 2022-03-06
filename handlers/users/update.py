from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from data import variables
from keyboards.inline.user.callback_datas import forms_callback
from keyboards.inline.user.continue_button import continue_button, accept_button
from keyboards.inline.user.forms_keyboard import create_forms_keyboard, create_forms_update_keyboard
from loader import dp, db, bot
from states.fill_in_form import FillInForms


@dp.message_handler(Command("update"))
async def on_command_update(message: types.Message, state: FSMContext):
    user = db.select_user_by_id(user_id=int(message.chat.id))
    if user is None:
        await bot.send_message(text=f"Привет, {message.from_user.full_name}!", chat_id=message.chat.id,
                               reply_markup=continue_button)
        try:
            db.add_user(int(message.chat.id))
        except Exception as err:
            print(err)
    else:
        if user[2] == "Inactive":
            await bot.send_message(chat_id=message.chat.id, text="Текст для ознакомления",
                                   reply_markup=accept_button)
        else:
            await FillInForms.Update.set()
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
            keyboard = create_forms_update_keyboard(options)
            await bot.send_message(chat_id=message.chat.id, text=question, reply_markup=keyboard)


@dp.callback_query_handler(forms_callback.filter(action="fill_in_form"), state=FillInForms.Update)
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
        text = "Отлично! Мы обновили Вашу анкету."
        await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.message_id)
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
