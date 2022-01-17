from aiogram.types import CallbackQuery

from filters import IsOwnerCall, IsAdminCall
from keyboards.inline.admin.admin_main_keyboard import admin_main_keyboard
from keyboards.inline.admin.list_of_questions_keyboard import create_list_of_questions_keyboard
from keyboards.inline.owner.owner_main_keyboard import owner_main_keyboard
from loader import dp, db, bot


@dp.callback_query_handler(IsOwnerCall(), text="change_questions")
@dp.callback_query_handler(IsAdminCall(), text="change_questions")
async def change_questions(call: CallbackQuery):
    await call.answer()
    questions = db.select_all_questions()
    text_begin = "На данный момент имеются следующие вопросы: \n\n"
    list_of_questions = ''
    if len(questions) > 0:
        list_of_questions += "\n".join([
            f"{str(num+1)}. {question[1]} ({question[2]})" for num, question in enumerate(questions)
        ])
    else:
        list_of_questions = 'Пока нет вопросов'
    text_end = '\n\nКликните на номер вопроса, чтобы редактировать'
    await bot.send_message(chat_id=call.message.chat.id, text=text_begin+list_of_questions+text_end,
                           reply_markup=create_list_of_questions_keyboard(questions))


@dp.callback_query_handler(IsOwnerCall(), text="to_admin_panel")
async def navigate_to_admin_panel(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.message.chat.id, text="Вам доступны следующие функции:",
                                message_id=call.message.message_id, reply_markup=owner_main_keyboard)


@dp.callback_query_handler(IsAdminCall(), text="to_admin_panel")
async def navigate_to_admin_panel(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.message.chat.id, text="Вам доступны следующие функции:",
                                message_id=call.message.message_id, reply_markup=admin_main_keyboard)




