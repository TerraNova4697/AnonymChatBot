from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.owner.owner_callback_datas import deletion_confirmed_callback


def create_confirm_del_keyboard(user_id):
    confirm_admin_deletion_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data=deletion_confirmed_callback
                                 .new(action="delete", user_id=str(user_id)))
        ],
        [
            InlineKeyboardButton(text="Нет", callback_data="cancel_del")
        ]
    ])
    return confirm_admin_deletion_keyboard
