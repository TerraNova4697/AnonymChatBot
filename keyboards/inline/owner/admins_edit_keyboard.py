from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.owner.owner_callback_datas import choose_admin_callback


def create_admins_edit_keyboard(admins):
    keyboard = InlineKeyboardMarkup()
    for admin in admins:
        keyboard.add(InlineKeyboardButton(text=f'{admin[2]} {admin[1]}', callback_data=choose_admin_callback
                                          .new(action="delete", user_id=admin[0])))
    keyboard.add(InlineKeyboardButton(text="Добавить администратора", callback_data='add_admin'))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="cancel"))
    return keyboard
