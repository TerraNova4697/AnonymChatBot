from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.owner.owner_callback_datas import confirm_new_manager_callback, decline_new_manager_callback


def create_keyboard_to_confirm(user_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Подтвердить", callback_data=confirm_new_manager_callback
                                 .new(action="confirm", user_id=user_id))
        ],
        [
            InlineKeyboardButton(text="Отклонить", callback_data=decline_new_manager_callback
                                 .new(action="decline", user_id=user_id))
        ]
    ])
    return keyboard
