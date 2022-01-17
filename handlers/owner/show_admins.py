from aiogram.types import CallbackQuery

from filters import IsOwnerCall
from keyboards.inline.owner.admins_edit_keyboard import create_admins_edit_keyboard
from keyboards.inline.owner.confirm_admin_deletion import create_confirm_del_keyboard
from keyboards.inline.owner.owner_callback_datas import choose_admin_callback, deletion_confirmed_callback
from keyboards.inline.owner.owner_main_keyboard import owner_main_keyboard
from loader import dp, db, bot

add_admin_text = "Сообщите администратору скрытую команду /admin105, которую нужно ввести в бот для активации " \
                 "возможностей администратора. \n\nВам придет уведомление для подтверждения с данными администратора."


@dp.callback_query_handler(IsOwnerCall(), text="edit_admin")
async def show_admins(call: CallbackQuery):
    admins = db.select_all_active_admins(status="Active")
    text_start = "Сейчас работают следующие администраторы: \n"
    list_of_admins = ''
    if len(admins) > 0:
        list_of_admins += "\n".join([
            f"{str(num + 1)}. {str(admin[2])} {str(admin[1])}" for num, admin in enumerate(admins)
        ])
    else:
        list_of_admins = "Пока нет администраторов"
    text_end = "\n\nКликните на имя, чтобы удалить"
    await bot.send_message(chat_id=call.message.chat.id,
                           text=text_start + list_of_admins + text_end,
                           reply_markup=create_admins_edit_keyboard(admins))


@dp.callback_query_handler(IsOwnerCall(), text='cancel')
async def cancel_edit(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, text="Вам доступны следующие функции:",
                                message_id=call.message.message_id, reply_markup=owner_main_keyboard)


@dp.callback_query_handler(IsOwnerCall(), text='add_admin')
async def add_admin(call: CallbackQuery):
    await call.answer()
    await bot.send_message(chat_id=call.message.chat.id, text=add_admin_text)


@dp.callback_query_handler(choose_admin_callback.filter(action="delete"), IsOwnerCall())
async def confirm_deletion(call: CallbackQuery, callback_data: dict):
    await call.answer()
    user_id = callback_data.get("user_id")
    admin = db.select_admin_by_user_id(user_id=int(user_id))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"Вы точно хотите удалить {admin[1]} {admin[0]}",
                                reply_markup=create_confirm_del_keyboard(user_id=user_id))


@dp.callback_query_handler(IsOwnerCall(), text="cancel_del")
async def cancel_deletion(call: CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    admins = db.select_all_active_admins(status="Active")
    text_start = "Сейчас работают следующие администраторы: \n"
    list_of_admins = ''
    if len(admins) > 0:
        list_of_admins += "\n".join([
            f"{str(num + 1)}. {str(admin[2])} {str(admin[1])}" for num, admin in enumerate(admins)
        ])
    else:
        list_of_admins = "Пока нет администраторов"
    text_end = "\n\nКликните на имя, чтобы удалить"
    await bot.send_message(chat_id=call.message.chat.id,
                           text=text_start + list_of_admins + text_end,
                           reply_markup=create_admins_edit_keyboard(admins))


@dp.callback_query_handler(deletion_confirmed_callback.filter(action="delete"), IsOwnerCall())
async def delete_admin(call: CallbackQuery, callback_data: dict):
    user_id = callback_data.get("user_id")
    db.inactivate_admin(user_id=int(user_id), status="Inactive")
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    admins = db.select_all_active_admins(status="Active")
    text_start = "Сейчас работают следующие администраторы: \n"
    list_of_admins = ''
    if len(admins) > 0:
        list_of_admins += "\n".join([
            f"{str(num + 1)}. {str(admin[2])} {str(admin[1])}" for num, admin in enumerate(admins)
        ])
    else:
        list_of_admins = "Пока нет администраторов"
    text_end = "\n\nКликните на имя, чтобы удалить"
    await bot.send_message(chat_id=call.message.chat.id,
                           text=text_start + list_of_admins + text_end,
                           reply_markup=create_admins_edit_keyboard(admins))




