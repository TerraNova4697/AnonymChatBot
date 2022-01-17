from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from data.variables import admins, owner
from filters import IsNotOwner
from keyboards.inline.admin.admin_main_keyboard import admin_main_keyboard
from keyboards.inline.cancel_button import cancel_button
from keyboards.inline.owner.admin_request import create_keyboard_to_confirm
from loader import dp, bot, db
from states.register_admin_states import RegisterAdmin

notify_admin_added = "Приветствую администратора! Вы можете выбрать следующие функции:"
notified_text = "Мы отправили ваш запрос на права администратора. Пожалуйста, дождитесь подтверждения."


@dp.message_handler(Command('admin105'), IsNotOwner())
async def register_admin(message: types.Message):
    if int(message.chat.id) in admins:
        await bot.send_message(chat_id=message.chat.id, text=notify_admin_added, reply_markup=admin_main_keyboard)
    else:
        await bot.send_message(chat_id=message.chat.id, text="Введите свою фамилию", reply_markup=cancel_button)
        await RegisterAdmin.InputName.set()


@dp.callback_query_handler(state=RegisterAdmin.InputName, text="cancel")
async def cancel_input_name(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=RegisterAdmin.InputName)
async def write_name(message: types.Message, state: FSMContext):
    await state.update_data({"surname": message.text})
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.chat.id, text="Введите свое имя", reply_markup=cancel_button)
    await RegisterAdmin.InputSurname.set()


@dp.callback_query_handler(state=RegisterAdmin.InputSurname, text="cancel")
async def cancel_input_surname(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()


@dp.message_handler(state=RegisterAdmin.InputSurname)
async def request_admin_access(message: types.Message, state: FSMContext):
    data = await state.get_data()
    surname = data.get("surname")
    name = message.text
    try:
        db.add_admin(user_id=int(message.chat.id), name=name, surname=surname)
        await bot.send_message(chat_id=owner[0],
                               text=f"Сотрудник {surname} {name} отправил запрос на права администратора.",
                               reply_markup=create_keyboard_to_confirm(int(message.chat.id)))
        await bot.send_message(chat_id=message.chat.id, text=notified_text)
    except Exception as err:
        print(err)
        await bot.send_message(chat_id=message.chat.id, text="Доступ отклонен")
    finally:
        await state.finish()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
