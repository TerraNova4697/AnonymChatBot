from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsAdminCall, IsOwnerCall
from keyboards.inline.admin.admin_callback_datas import choose_f_question_callback
from keyboards.inline.admin.edit_f_question_keyboard import create_edit_f_question_keyboard
from keyboards.inline.admin.list_of_f_questions_keyboard import create_list_of_forms_questions_keyboard
from loader import dp, bot, db
from states.AddFormQuestion import AddFormQuestion


@dp.callback_query_handler(IsOwnerCall(), text="change_form")
@dp.callback_query_handler(IsAdminCall(), text="change_form")
async def change_questions(call: CallbackQuery):
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


@dp.callback_query_handler(IsOwnerCall(), choose_f_question_callback.filter(action="choose_f_quest"))
@dp.callback_query_handler(IsAdminCall(), choose_f_question_callback.filter(action="choose_f_quest"))
async def edit_f_question(call: CallbackQuery, state: FSMContext, callback_data: dict):
    f_questions_id = callback_data.get("f_question_id")
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
