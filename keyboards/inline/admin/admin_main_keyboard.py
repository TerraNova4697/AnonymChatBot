from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_main_keyboard = InlineKeyboardMarkup(row_width=1,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text='Изменить вопросы собеседников',
                                                                        callback_data="change_questions")
                                               ],
                                               [
                                                   InlineKeyboardButton(text='Изменить вопросы анкеты',
                                                                        callback_data="change_form")
                                               ]
                                           ])
