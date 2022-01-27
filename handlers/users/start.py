from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data import variables
from keyboards.inline.user.callback_datas import quiz_callback
from keyboards.inline.user.continue_button import continue_button, accept_button, try_again_button
from keyboards.inline.user.quiz_keyboard import create_quiz_keyboard
from loader import dp, bot, db
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
                                        text="Вы успешно прошли тестирование")
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


