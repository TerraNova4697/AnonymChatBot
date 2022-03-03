from aiogram.types import CallbackQuery

from data import variables
from keyboards.inline.user.partner_search_lifecycle import create_keyboard_back_to_partner_search
from loader import dp, db, bot
from utils.misc.user import User


@dp.callback_query_handler(text="deny_partn")
async def on_deny_partner_clicked(call: CallbackQuery):
    for user in variables.users_search_queue:
        if user.user_id == int(call.message.chat.id):
            if user.status == "FoundPartner":
                await bot.edit_message_text(text="Мы подбираем для Вас человека. Это может занять некоторое время, "
                                                 "Вам придет уведомление, когда мы найдем.",
                                            message_id=call.message.message_id, chat_id=call.message.chat.id)
                db.update_users_status_and_partner_id(status="InSearch", partner_id=0, user_id=call.message.chat.id)
                for partner in variables.users_search_queue:
                    if partner.user_id == user.partner_id:
                        if partner.status == "AcceptedPartner":
                            await bot.send_message(
                                text="К сожалению собеседник отказался от общения. \n\n"
                                     "Мы подбираем для Вас человека. Это может занять некоторое время, "
                                     "Вам придет уведомление, когда мы найдем.",
                                chat_id=partner.user_id)
                            db.update_users_status_and_partner_id(status="InSearch", partner_id=0,
                                                                  user_id=partner.user_id)
                            partner.status = "InSearch"
                            partner.denied_partners.append(user.user_id)
                            user.partner_id = 0
                user.status = "InSearch"
                user.denied_partners.append(user.partner_id)
                user.partner_id = 0


@dp.callback_query_handler(text="accept_partn")
async def on_accept_partner_clicked(call: CallbackQuery):
    print("on_accept_partner_clicked")
    for user in variables.users_search_queue:
        if user.user_id == int(call.message.chat.id):
            user.status = "AcceptedPartner"
            print(user.status)
            for partner in variables.users_search_queue:
                print(f"partner.status = {partner.status}")
                print(f"partner.user_id = {partner.user_id}")
                if partner.user_id == user.partner_id:
                    if partner.status == "InSearch":
                        print("partner.status = InSearch(condition 1)")
                        await bot.edit_message_text(
                            text="К сожалению собеседник отказался от общения. \n\n"
                                 "Мы подбираем для Вас человека. Это может занять некоторое время, "
                                 "Вам придет уведомление, когда мы найдем.",
                            message_id=call.message.message_id, chat_id=call.message.chat.id)
                        db.update_users_status_and_partner_id(status="InSearch", partner_id=0,
                                                              user_id=call.message.chat.id)
                        user.status = "InSearch"
                        user.denied_partners.append(user.partner_id)
                        user.partner_id = 0
                    elif partner.status == "FoundPartner":
                        print("partner.status = FoundPartner(condition 2)")
                        await bot.edit_message_text(text="Собеседник пока что не ответил. "
                                                         "Мы уведомим Вас как только он ответит.",
                                                    chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                    reply_markup=create_keyboard_back_to_partner_search())
                    elif partner.status == "AcceptedPartner":
                        print("partner.status = AcceptedPartner(condition 3)")
                        await bot.edit_message_text(text="Собеседник также принял Вас. Выбрать уровень откровенности",
                                                    chat_id=call.message.chat.id, message_id=call.message.message_id)
                        await bot.send_message(chat_id=partner.user_id, text="Собеседник также принял Вас. Выбрать уровень откровенности")


@dp.callback_query_handler(text="cancel_partner")
async def on_cancel_partner_clicked(call: CallbackQuery):
    for user in variables.users_search_queue:
        if user.user_id == int(call.message.chat.id):
            if user.status == "AcceptedPartner":
                await bot.edit_message_text(text="Мы подбираем для Вас человека. Это может занять некоторое время, "
                                                 "Вам придет уведомление, когда мы найдем.",
                                            message_id=call.message.message_id, chat_id=call.message.chat.id)
                db.update_users_status_and_partner_id(status="InSearch", partner_id=0, user_id=call.message.chat.id)
                user.status = "InSearch"
                user.denied_partners.append(user.partner_id)
                user.partner_id = 0
