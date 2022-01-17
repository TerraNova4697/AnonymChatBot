from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.admin.admin_callback_datas import edit_category_keyboard
from loader import db


def create_edit_category_keyboard():
    categories = db.select_all_question_categories()
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton(text="Без категории", callback_data=edit_category_keyboard
                                         .new(action="edit_cat", category="Без категории")))
    for index, category in enumerate(categories):
        keyboard.insert(InlineKeyboardButton(text=f"{category[0]}", callback_data=edit_category_keyboard
                                             .new(action="edit_cat", category=f"{category[0]}")))
    keyboard.row(InlineKeyboardButton(text="Отмена", callback_data="cancel"))
    return keyboard
