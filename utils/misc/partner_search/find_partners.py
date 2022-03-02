from aiogram import Bot

from data import variables
from keyboards.inline.user.partner_search_lifecycle import create_keyboard_found_partner
from loader import db
from utils.misc.user import User


async def find_partner(bot: Bot):
    for user in variables.users_search_queue:
        important_values = db.select_all_users_filled_forms(user_id=user.user_id, is_important="True")
        for searched_user in variables.users_search_queue:
            if searched_user.user_id != user.user_id and searched_user.user_id not in user.denied_partners:
                partners_value = 0
                for value in important_values:
                    print(f"value - {value}")
                    answer_value = db.select_users_filled_form(user_id=searched_user.user_id,
                                                               f_answer_id=value[4])
                    if answer_value[4] == value[6]:
                        partners_value += 1
                if partners_value >= 2:
                    partners_important_values = db.select_all_users_filled_forms(user_id=searched_user.user_id,
                                                                                 is_important="True")
                    users_value = 0
                    for value in partners_important_values:
                        answer_value = db.select_users_filled_form(user_id=user.user_id,
                                                                   f_answer_id=value[4])
                        if answer_value[4] == value[6]:
                            users_value += 1
                    if partners_value >= 2 and users_value >= 2:
                        users_text = 'Мы нашли для Вас собеседника.\nОзнакомьтесь с его данными: \n\n'
                        for value in important_values:
                            answer_value = db.select_users_filled_form(user_id=searched_user.user_id,
                                                                       f_answer_id=value[4])
                            users_text = users_text + answer_value[3] + '\n'
                            f_answer = db.select_f_answer_text_by_id(answer_id=answer_value[4])
                            users_text = users_text + f_answer[0] + '\n\n'
                        db.update_users_status_and_partner_id(status="FoundPartner", partner_id=searched_user.user_id,
                                                              user_id=user.user_id)
                        await bot.send_message(chat_id=user.user_id, text=users_text,
                                               reply_markup=create_keyboard_found_partner(searched_user.user_id))
                        partners_text = 'Мы нашли для Вас собеседника.\nОзнакомьтесь с его данными: \n\n'
                        for value in partners_important_values:
                            answer_value = db.select_users_filled_form(user_id=user.user_id,
                                                                       f_answer_id=value[4])
                            partners_text = partners_text + answer_value[3] + '\n'
                            f_answer = db.select_f_answer_text_by_id(answer_id=answer_value[4])
                            partners_text = partners_text + f_answer[0] + '\n\n'
                        db.update_users_status_and_partner_id(status="FoundPartner", partner_id=user.user_id,
                                                              user_id=searched_user.user_id)
                        await bot.send_message(chat_id=searched_user.user_id, text=partners_text,
                                               reply_markup=create_keyboard_found_partner(user.user_id))
                        variables.users_search_queue.remove(user)
                        variables.users_search_queue.remove(searched_user)
                    else:
                        if not user.is_notified:
                            await bot.send_message(chat_id=user.user_id, text=f"Мы еще подбираем для Вас собеседника")
                            user.is_notified = True
