from aiogram.types import CallbackQuery

from data import variables
from data.variables import openness_levels
from keyboards.default.chat_keyboard import create_chat_keyboard
from keyboards.inline.user.callback_datas import choose_openness_callback
from keyboards.inline.user.partner_search_lifecycle import create_keyboard_back_to_partner_search, \
    create_keyboard_choose_openness, create_keyboard_accept_partners_openness, create_keyboard_search_new_partner
from loader import dp, db, bot


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
                        db.add_new_chat(partner1_id=int(call.message.chat.id), partner2_id=partner.user_id)
                        await bot.edit_message_text(text="Собеседник также принял Вас. Выбрите уровень откровенности",
                                                    chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                    reply_markup=create_keyboard_choose_openness())
                        await bot.send_message(chat_id=partner.user_id,
                                               text="Собеседник также принял Вас. Выбрите уровень откровенности",
                                               reply_markup=create_keyboard_choose_openness())


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


# Выбор уровня откровенности
@dp.callback_query_handler(choose_openness_callback.filter(action="openness"))
async def on_choose_openness_clicked(call: CallbackQuery, callback_data: dict):
    openness = callback_data.get("choice")
    chat = db.select_chat_by_partner_id(partner1_id=int(call.message.chat.id), partner2_id=int(call.message.chat.id))
    if chat is not None:
        if chat[3] == "":
            db.update_chat_openness(openness=openness, chat_id=chat[0])
            await bot.edit_message_text(text=f"Отличено, Вы выбрали уровень откровения - {openness}\n\n"
                                             f"Собеседник еще не определился с уровнем.", chat_id=call.message.chat.id,
                                        message_id=call.message.message_id)
        elif chat[3] != "":
            users_level = openness_levels[openness]
            partners_level = openness_levels[chat[3]]
            if users_level > partners_level:
                await bot.edit_message_text(text=f'Ваш собеседник выбрал уровень откровения ниже - {chat[3]}\n\n'
                                                 f'Вы согласны начать с него или хотите поискать другого собеседника?',
                                            chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=create_keyboard_accept_partners_openness())
            elif users_level < partners_level:
                db.update_chat_openness(openness=openness, chat_id=chat[0])
                await bot.edit_message_text(text="Ваш собеседник выбрал уровень откровения выше. "
                                                 "Мы предолжим ему Ваш уровень.", chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=create_keyboard_search_new_partner())
                if chat[1] == int(call.message.chat.id):
                    await bot.send_message(chat_id=chat[2],
                                           text=f'Ваш собеседник выбрал уровень откровения ниже - {openness}\n\n'
                                                f'Вы согласны начать с него или хотите поискать другого собеседника?',
                                           reply_markup=create_keyboard_accept_partners_openness())
                elif chat[2] == int(call.message.chat.id):
                    await bot.send_message(chat_id=chat[1],
                                           text=f'Ваш собеседник выбрал уровень откровения ниже - {chat[3]}\n\n'
                                                f'Вы согласны начать с него или хотите поискать другого собеседника?',
                                           reply_markup=create_keyboard_accept_partners_openness())
            elif users_level == partners_level:
                db.update_chat_status(status="Conversation", chat_id=chat[0])
                await bot.send_message(chat_id=chat[1], text=f"Отлично, уровень откровенности Вашей беседы - {chat[3]}"
                                                             f"\n\nВы можете писать сообщения, а также в меню выбрать "
                                                             f"вопрос из библиотеки, если у Вас закончились темы для "
                                                             f"обсуждения.", reply_markup=create_chat_keyboard())
                await bot.send_message(chat_id=chat[2], text=f"Отлично, уровень откровенности Вашей беседы - {chat[3]}"
                                                             f"\n\nВы можете писать сообщения, а также в меню выбрать "
                                                             f"вопрос из библиотеки, если у Вас закончились темы для "
                                                             f"обсуждения.", reply_markup=create_chat_keyboard())
    else:
        for user in variables.users_search_queue:
            if user.user_id == int(call.message.chat.id):
                await bot.edit_message_text(
                    text="Ваш собеседник отказался от общения на этом уровне откровенности. \n\n"
                         "Мы подбираем для Вас человека. Это может занять некоторое время, "
                         "Вам придет уведомление, когда мы найдем.",
                    message_id=call.message.message_id, chat_id=call.message.chat.id)
                db.update_users_status_and_partner_id(status="InSearch", partner_id=0,
                                                      user_id=call.message.chat.id)
                user.status = "InSearch"
                user.denied_partners.append(user.partner_id)
                user.partner_id = 0


@dp.callback_query_handler(text="accept_level")
async def on_accept_level_clicked(call: CallbackQuery):
    chat = db.select_chat_by_partner_id(partner1_id=int(call.message.chat.id), partner2_id=int(call.message.chat.id))
    if chat is not None:
        db.update_chat_status(status="Conversation", chat_id=chat[0])
        await bot.send_message(chat_id=chat[1], text=f"Отлично, уровень откровенности Вашей беседы - {chat[3]}"
                                                     f"\n\nВы можете писать сообщения, а также в меню выбрать "
                                                     f"вопрос из библиотеки, если у Вас закончились темы для "
                                                     f"обсуждения.", reply_markup=create_chat_keyboard())
        await bot.send_message(chat_id=chat[2], text=f"Отлично, уровень откровенности Вашей беседы - {chat[3]}"
                                                     f"\n\nВы можете писать сообщения, а также в меню выбрать "
                                                     f"вопрос из библиотеки, если у Вас закончились темы для "
                                                     f"обсуждения.", reply_markup=create_chat_keyboard())
    else:
        for user in variables.users_search_queue:
            if user.user_id == int(call.message.chat.id):
                await bot.edit_message_text(
                    text="Ваш собеседник отказался от общения на этом уровне откровенности. \n\n"
                         "Мы подбираем для Вас человека. Это может занять некоторое время, "
                         "Вам придет уведомление, когда мы найдем.",
                    message_id=call.message.message_id, chat_id=call.message.chat.id)
                db.update_users_status_and_partner_id(status="InSearch", partner_id=0,
                                                      user_id=call.message.chat.id)
                user.status = "InSearch"
                user.denied_partners.append(user.partner_id)
                user.partner_id = 0


@dp.callback_query_handler(text="search_partner")
async def on_search_partner_clicked(call: CallbackQuery):
    for user in variables.users_search_queue:
        if user.user_id == int(call.message.chat.id):
            if user.status == "AcceptedPartner":
                db.delete_chat_by_partner_id(partner1_id=int(call.message.chat.id),
                                             partner2_id=int(call.message.chat.id))
                await bot.edit_message_text(text="Мы подбираем для Вас человека. Это может занять некоторое время, "
                                                 "Вам придет уведомление, когда мы найдем.",
                                            message_id=call.message.message_id, chat_id=call.message.chat.id)
                db.update_users_status_and_partner_id(status="InSearch", partner_id=0, user_id=call.message.chat.id)
                user.status = "InSearch"
                user.denied_partners.append(user.partner_id)
                user.partner_id = 0



