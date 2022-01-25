from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from data.variables import test
from filters import IsAdminCall, IsOwnerCall
from keyboards.inline.admin.admin_callback_datas import delete_test_question_callback, \
    confirm_test_question_deletion_callback
from keyboards.inline.admin.edit_test_question_keyboard import create_edit_test_question_keyboard
from loader import dp, bot, db
from states.edit_test_question import EditTestQuestion
from utils.prepare_text_keyboard_edit_test import create_options_text_for_editing, create_text_and_keyboard


@dp.callback_query_handler(IsAdminCall(), delete_test_question_callback.filter(action="del_t_quest"),
                           state=EditTestQuestion.Edit)
@dp.callback_query_handler(IsOwnerCall(), delete_test_question_callback.filter(action="del_t_quest"),
                           state=EditTestQuestion.Edit)
async def on_back_clicked(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить", callback_data=confirm_test_question_deletion_callback
                                 .new(action="confirmed", question_id=question_id)),
            InlineKeyboardButton(text="Отмена", callback_data=confirm_test_question_deletion_callback
                                 .new(action="cancel", question_id=question_id))
        ]
    ])
    await bot.send_message(chat_id=call.message.chat.id, text="Вы действительно хотите удалить данный вопрос?",
                           reply_markup=keyboard)
    await EditTestQuestion.Delete.set()


@dp.callback_query_handler(IsAdminCall(), confirm_test_question_deletion_callback.filter(action="cancel"),
                           state=EditTestQuestion.Delete)
@dp.callback_query_handler(IsOwnerCall(), confirm_test_question_deletion_callback.filter(action="cancel"),
                           state=EditTestQuestion.Delete)
async def cancel_deletion(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    text = db.select_test_question_text(question_id=question_id)
    question_text = text[0]
    options = db.select_all_test_answers(question_id=question_id)
    options_text = create_options_text_for_editing(options)
    keyboard = create_edit_test_question_keyboard(options)
    await bot.send_message(chat_id=call.message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await EditTestQuestion.Edit.set()


@dp.callback_query_handler(IsAdminCall(), confirm_test_question_deletion_callback.filter(action="confirmed"),
                           state=EditTestQuestion.Delete)
@dp.callback_query_handler(IsOwnerCall(), confirm_test_question_deletion_callback.filter(action="confirmed"),
                           state=EditTestQuestion.Delete)
async def delete_test_question(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    question_id = callback_data.get("question_id")
    question_text = db.select_test_question_text(question_id=int(question_id))
    test.pop(question_text[0])
    db.delete_test_question(question_id=int(question_id))
    text, keyboard = create_text_and_keyboard()
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard)
    await state.finish()
