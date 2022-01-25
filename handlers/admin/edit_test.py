from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsOwnerCall, IsAdminCall
from keyboards.inline.admin.admin_callback_datas import edit_test_callback, delete_test_question_callback
from keyboards.inline.admin.admin_main_keyboard import admin_main_keyboard
from keyboards.inline.admin.edit_test_question_keyboard import edit_test_question_keyboard, \
    create_edit_test_question_keyboard
from keyboards.inline.owner.owner_main_keyboard import owner_main_keyboard
from loader import dp, bot, db
from states.edit_test_question import EditTestQuestion
from utils.prepare_text_keyboard_edit_test import create_text_and_keyboard, create_options_text, \
    create_options_text_for_editing


@dp.callback_query_handler(IsOwnerCall(), text="change_test")
@dp.callback_query_handler(IsAdminCall(), text="change_test")
async def on_edit_test_command(call: CallbackQuery):
    await call.answer()
    text, keyboard = create_text_and_keyboard()
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard)


@dp.callback_query_handler(IsOwnerCall(), text="test_to_main")
async def navigate_to_admin_panel(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.message.chat.id, text="Вам доступны следующие функции:",
                                message_id=call.message.message_id, reply_markup=owner_main_keyboard)


@dp.callback_query_handler(IsAdminCall(), text="test_to_main")
async def navigate_to_admin_panel(call: CallbackQuery):
    await call.answer()
    await bot.edit_message_text(chat_id=call.message.chat.id, text="Вам доступны следующие функции:",
                                message_id=call.message.message_id, reply_markup=admin_main_keyboard)


@dp.callback_query_handler(IsAdminCall(), edit_test_callback.filter(action="edit_test"))
@dp.callback_query_handler(IsOwnerCall(), edit_test_callback.filter(action="edit_test"))
async def on_question_clicked(call: CallbackQuery, callback_data: dict):
    question_id = callback_data.get("question_id")
    text = db.select_test_question_text(question_id=question_id)
    question_text = text[0]
    options = db.select_all_test_answers(question_id=question_id)
    options_text = create_options_text_for_editing(options)
    keyboard = create_edit_test_question_keyboard(options)
    await bot.send_message(chat_id=call.message.chat.id, text=f"{question_text}\n\nВарианты ответов:\n\n{options_text}",
                           reply_markup=keyboard)
    await EditTestQuestion.Edit.set()


@dp.callback_query_handler(IsAdminCall(), text='nav_to_t_quest', state=EditTestQuestion.Edit)
@dp.callback_query_handler(IsOwnerCall(), text='nav_to_t_quest', state=EditTestQuestion.Edit)
async def on_back_clicked(call: CallbackQuery, state: FSMContext):
    await call.answer()
    text, keyboard = create_text_and_keyboard()
    await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=keyboard)
    await state.finish()




