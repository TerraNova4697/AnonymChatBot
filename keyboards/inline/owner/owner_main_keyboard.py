from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

owner_main_keyboard = InlineKeyboardMarkup(row_width=1,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text="Редактировать список администраторов",
                                                                        callback_data="edit_admin")
                                               ],
                                               [
                                                    InlineKeyboardButton(text="Редактировать вопросы теста",
                                                                         callback_data="change_test")
                                               ],
                                               [
                                                   InlineKeyboardButton(text='Изменить вопросы собеседников',
                                                                        callback_data="change_questions")
                                               ],
                                               [
                                                   InlineKeyboardButton(text='Изменить вопросы анкеты',
                                                                        callback_data="change_form")
                                               ]
                                           ])
