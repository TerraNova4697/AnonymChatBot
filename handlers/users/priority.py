from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.user.important_form_answers_keyboard import create_important_form_answers_keyboard
from loader import dp, db, bot
from states.fill_in_form import FillInForms


@dp.message_handler(Command("priority"))
async def on_priority_clicked(message: types.Message):
    user = db.select_user_by_id(user_id=int(message.chat.id))
    print(user)
    if user[2] != "Inactive":
        text_begin = "Теперь выберите 3 важные критерия для Вас при поиске " \
                     "собеседника, кликнув на них по очереди.\n\n" \
                     "Если Вы хотите убрать какой-то критерий, кликните на него еще раз\n\n"
        unfilled_form = db.select_all_users_filled_forms(user_id=message.chat.id)
        text, keyboard = create_important_form_answers_keyboard(unfilled_form)
        await bot.send_message(chat_id=message.chat.id, text=text_begin + text,
                               reply_markup=keyboard)
        await FillInForms.ChooseImportant.set()
