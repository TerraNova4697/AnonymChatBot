from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from data.variables import admins
from filters import IsOwnerCall
from keyboards.inline.admin.admin_main_keyboard import admin_main_keyboard
from keyboards.inline.owner.owner_callback_datas import confirm_new_manager_callback, decline_new_manager_callback
from loader import dp, bot, db

notify_admin_added = "Приветствую администратора! Вы можете выбрать следующие функции:"


@dp.callback_query_handler(confirm_new_manager_callback.filter(action="confirm"), IsOwnerCall())
async def give_admin_access(call: CallbackQuery, callback_data: dict):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    admin_id = callback_data.get("user_id")
    admin = db.select_admin_by_user_id(user_id=int(admin_id))
    print(admin)
    db.update_admin(user_id=int(admin_id), status="Active")
    await bot.send_message(chat_id=call.message.chat.id,
                           text=f"Пользователь {admin[1]} {admin[0]}"
                                f" принят в качестве администратора")
    admins.append(int(admin_id))
    await bot.send_message(chat_id=admin_id, text=notify_admin_added, reply_markup=admin_main_keyboard)


@dp.callback_query_handler(decline_new_manager_callback.filter(action="decline"), IsOwnerCall())
async def decline_admin_access(call: CallbackQuery, callback_data: dict):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    admin_id = callback_data.get("user_id")
    admin = db.select_admin_by_user_id(user_id=int(admin_id))
    await bot.send_message(chat_id=call.message.chat.id,
                           text=f"Пользователь {admin[1]} {admin[0]}"
                                f" не является администратором.")
    await bot.send_message(chat_id=admin_id, text="Доступ отклонен")
