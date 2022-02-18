from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from data import variables
from loader import dp, bot, db


@dp.message_handler(text="Анкета")
async def forms(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=variables.f_questions)


@dp.message_handler(Command('delete_users'))
async def del_users(message: types.Message):
    db.delete_users()
    db.delete_filled_forms()
    users = db.select_all_users()

    await bot.send_message(chat_id=message.chat.id, text=str(users))
