from aiogram.types import CallbackQuery

from filters import IsAdminCall, IsOwnerCall
from keyboards.inline.admin.list_of_f_questions_keyboard import create_list_of_forms_questions_keyboard
from loader import dp, bot, db


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
