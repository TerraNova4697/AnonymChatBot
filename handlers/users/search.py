from aiogram import types
from aiogram.dispatcher.filters import Command

from data import variables
from loader import dp, db, bot


@dp.message_handler(Command("search"))
async def on_search_command(message: types.Message):
    user = db.select_user_by_id(user_id=int(message.chat.id))
    if user[2] == "FoundPartner" or user[2] == "AcceptedPartner":
        for user in variables.users_search_queue:
            if user.user_id == int(message.chat.id):
                db.delete_chat_by_partner_id(partner1_id=int(message.chat.id),
                                             partner2_id=int(message.chat.id))
                await bot.send_message(text="Мы подбираем для Вас человека. Это может занять некоторое время, "
                                            "Вам придет уведомление, когда мы найдем.",
                                       chat_id=message.chat.id)
                db.update_users_status_and_partner_id(status="InSearch", partner_id=0, user_id=int(message.chat.id))
                await bot.send_message(chat_id=user.partner_id, text="Ваш собеседник покинул чат. "
                                                                     "Мы подбираем для Вас человека. Это может занять некоторое время, "
                                                                     "Вам придет уведомление, когда мы найдем.", )
                db.update_users_status_and_partner_id(status="InSearch", partner_id=0, user_id=user.partner_id)
                for partner in variables.users_search_queue:
                    if partner.user_id == user.partner_id:
                        partner.status = "InSearch"
                        partner.denied_partners.append(partner.partner_id)
                        partner.partner_id = 0
                user.status = "InSearch"
                user.denied_partners.append(user.partner_id)
                user.partner_id = 0



