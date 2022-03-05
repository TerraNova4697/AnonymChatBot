from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_chat_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            KeyboardButton(text="Получить вопрос")
        ]
    ])
    return keyboard
