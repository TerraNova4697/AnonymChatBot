from aiogram.types import CallbackQuery

from data import variables
from loader import dp, db, bot
from utils.misc.user import User


@dp.callback_query_handler(text="begin_search")
async def add_user_to_search_queue(call: CallbackQuery):
    await bot.edit_message_text(text="Мы подбираем для Вас человека. Это может занять некоторое вреся, "
                                     "Вам придет уведомление, когда мы найдем.",
                                message_id=call.message.message_id, chat_id=call.message.chat.id)
    db.update_users_status_in_search(status="InSearch", user_id=call.message.chat.id)
    current_user = db.select_user_by_id(user_id=int(call.message.chat.id))
    new_user_to_queue = User()
    new_user_to_queue.user_id = current_user[0]
    new_user_to_queue.name = current_user[1]
    new_user_to_queue.status = current_user[2]
    variables.users_search_queue.append(new_user_to_queue)

