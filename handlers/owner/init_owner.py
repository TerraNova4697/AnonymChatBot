from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsOwner
from keyboards.inline.owner.owner_main_keyboard import owner_main_keyboard
from loader import dp, bot

say_hello_text = 'Приветствую владельца!\n\nВам доступны следующие функции:'


@dp.message_handler(Command("owner"), IsOwner())
async def init_owner(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=say_hello_text, reply_markup=owner_main_keyboard)
