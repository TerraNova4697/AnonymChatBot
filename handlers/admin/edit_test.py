
from aiogram.types import CallbackQuery

from filters import IsOwnerCall, IsAdminCall
from keyboards.inline.admin.admin_main_keyboard import admin_main_keyboard
from keyboards.inline.owner.owner_main_keyboard import owner_main_keyboard
from loader import dp, bot
from utils.prepare_text_keyboard_edit_test import create_text_and_keyboard


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

