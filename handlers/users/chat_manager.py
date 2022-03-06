from aiogram import types
from aiogram.types import ContentType, CallbackQuery
import random

from data import variables
from filters import IsInConversation
from filters.is_in_conversation import IsInConversationGetQuestion, IsInConversationCall
from keyboards.inline.user.chat_lifecycle_keyboard import create_keyboard_pass_question, \
    create_keyboard_answered_all_questions
from loader import dp, db, bot


@dp.message_handler(IsInConversation())
async def on_message_received(message: types.Message):
    chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                        partner2_id=int(message.chat.id))
    if chat[1] == int(message.chat.id):
        await bot.send_message(chat_id=chat[2],
                               text=message.text)
    elif chat[2] == int(message.chat.id):
        await bot.send_message(chat_id=chat[1],
                               text=message.text)


@dp.message_handler(IsInConversation(), content_types=ContentType.PHOTO)
async def on_message_received(message: types.Message):
    chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                        partner2_id=int(message.chat.id))
    if chat[1] == int(message.chat.id):
        await bot.send_photo(chat_id=chat[2], photo=message.photo[-1].file_id, caption=message.caption)
    elif chat[2] == int(message.chat.id):
        await bot.send_photo(chat_id=chat[1], photo=message.photo[-1].file_id, caption=message.caption)


@dp.message_handler(IsInConversation(), content_types=ContentType.VIDEO)
async def on_message_received(message: types.Message):
    chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                        partner2_id=int(message.chat.id))
    if chat[1] == int(message.chat.id):
        await bot.send_video(chat_id=chat[2], video=message.video.file_id, caption=message.caption)
    elif chat[2] == int(message.chat.id):
        await bot.send_video(chat_id=chat[1], video=message.video.file_id, caption=message.caption)


@dp.message_handler(IsInConversation(), content_types=ContentType.AUDIO)
async def on_message_received(message: types.Message):
    chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                        partner2_id=int(message.chat.id))
    if chat[1] == int(message.chat.id):
        await bot.send_audio(chat_id=chat[2], audio=message.audio.file_id)
    elif chat[2] == int(message.chat.id):
        await bot.send_audio(chat_id=chat[1], audio=message.audio.file_id)


@dp.message_handler(IsInConversation(), content_types=ContentType.ANIMATION)
async def on_message_received(message: types.Message):
    chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                        partner2_id=int(message.chat.id))
    if chat[1] == int(message.chat.id):
        await bot.send_animation(chat_id=chat[2], animation=message.animation.file_id)
    elif chat[2] == int(message.chat.id):
        await bot.send_animation(chat_id=chat[1], animation=message.animation.file_id)


@dp.message_handler(IsInConversation(), content_types=ContentType.STICKER)
async def on_message_received(message: types.Message):
    chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                        partner2_id=int(message.chat.id))
    if chat[1] == int(message.chat.id):
        await bot.send_sticker(chat_id=chat[2], sticker=message.sticker.file_id)
    elif chat[2] == int(message.chat.id):
        await bot.send_sticker(chat_id=chat[1], sticker=message.sticker.file_id)


@dp.message_handler(IsInConversation(), content_types=ContentType.VOICE)
async def on_message_received(message: types.Message):
    chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                        partner2_id=int(message.chat.id))
    if chat[1] == int(message.chat.id):
        await bot.send_voice(chat_id=chat[2], voice=message.voice.file_id)
    elif chat[2] == int(message.chat.id):
        await bot.send_voice(chat_id=chat[1], voice=message.voice.file_id)


@dp.message_handler(IsInConversationGetQuestion())
async def on_get_question_slicked(message: types.Message):
    chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                        partner2_id=int(message.chat.id))
    answered_questions = chat[8].split()
    print(answered_questions)
    print(chat[3])
    if chat[3] == "Формальный":
        count = 1
        question = random.choice(variables.formal_questions)
        if str(question[0]) in answered_questions:
            while str(question[0]) in answered_questions:
                print("Formal - inside while loop")
                count += 1
                if count >= len(variables.formal_questions) or count > len(variables.formal_questions):
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[2],
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?", reply_markup=create_keyboard_answered_all_questions())
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?", reply_markup=create_keyboard_answered_all_questions())
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[1],
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?", reply_markup=create_keyboard_answered_all_questions())
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?",
                                               reply_markup=create_keyboard_answered_all_questions())
                    break
                question = random.choice(variables.formal_questions)
                if str(question[0]) not in answered_questions:
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[2],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[1],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])
                    break
        else:
            if chat[1] == int(message.chat.id):
                await bot.send_message(chat_id=chat[2],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            elif chat[2] == int(message.chat.id):
                await bot.send_message(chat_id=chat[1],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])
    elif chat[3] == "Приятельский":
        count = 1
        question = random.choice(variables.fellowish_questions)
        if str(question[0]) in answered_questions:
            while str(question[0]) in answered_questions:
                count += 1
                if count >= len(variables.fellowish_questions):
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[2],
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?", reply_markup=create_keyboard_answered_all_questions())
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?",
                                               reply_markup=create_keyboard_answered_all_questions())
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[1],
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?", reply_markup=create_keyboard_answered_all_questions())
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?",
                                               reply_markup=create_keyboard_answered_all_questions())
                    break
                question = random.choice(variables.fellowish_questions)
                if str(question[0]) not in answered_questions:
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[2],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[1],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])
                    break
        else:
            if chat[1] == int(message.chat.id):
                await bot.send_message(chat_id=chat[2],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            elif chat[2] == int(message.chat.id):
                await bot.send_message(chat_id=chat[1],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])
    elif chat[3] == "Дружеский":
        count = 1
        question = random.choice(variables.friendly_questions)
        if str(question[0]) in answered_questions:
            while str(question[0]) in answered_questions:
                count += 1
                if count >= len(variables.friendly_questions):
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[2],
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?", reply_markup=create_keyboard_answered_all_questions())
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?",
                                               reply_markup=create_keyboard_answered_all_questions())
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[1],
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?", reply_markup=create_keyboard_answered_all_questions())
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?",
                                               reply_markup=create_keyboard_answered_all_questions())
                    break
                question = random.choice(variables.friendly_questions)
                if str(question[0]) not in answered_questions:
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[2],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[1],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])
                    break
        else:
            if chat[1] == int(message.chat.id):
                await bot.send_message(chat_id=chat[2],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            elif chat[2] == int(message.chat.id):
                await bot.send_message(chat_id=chat[1],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])
    elif chat[3] == "Близость":
        count = 1
        question = random.choice(variables.close_friend_questions)
        if str(question[0]) in answered_questions:
            while str(question[0]) in answered_questions:
                count += 1
                if count >= len(variables.close_friend_questions):
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[2],
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?", reply_markup=create_keyboard_answered_all_questions())
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?",
                                               reply_markup=create_keyboard_answered_all_questions())
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[1],
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?", reply_markup=create_keyboard_answered_all_questions())
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы. Вы готовы перейти на следующий уровень"
                                                    "откровенности?",
                                               reply_markup=create_keyboard_answered_all_questions())
                    break
                question = random.choice(variables.close_friend_questions)
                if str(question[0]) not in answered_questions:
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[2],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[1],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])
                    break
        else:
            if chat[1] == int(message.chat.id):
                await bot.send_message(chat_id=chat[2],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            elif chat[2] == int(message.chat.id):
                await bot.send_message(chat_id=chat[1],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])
    elif chat[3] == "Исповедь":
        count = 1
        question = random.choice(variables.confession_questions)
        if str(question[0]) in answered_questions:
            while str(question[0]) in answered_questions:
                count += 1
                if count >= len(variables.confession_questions):
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы.")
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=message.chat.id,
                                               text="Вы ответили на все вопросы.")
                    break
                question = random.choice(variables.confession_questions)
                if str(question[0]) not in answered_questions:
                    if chat[1] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[2],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    elif chat[2] == int(message.chat.id):
                        await bot.send_message(chat_id=chat[1],
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                        await bot.send_message(chat_id=message.chat.id,
                                               text=question[1], reply_markup=create_keyboard_pass_question())
                    db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])
                    break
        else:
            if chat[1] == int(message.chat.id):
                await bot.send_message(chat_id=chat[2],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            elif chat[2] == int(message.chat.id):
                await bot.send_message(chat_id=chat[1],
                                       text=question[1], reply_markup=create_keyboard_pass_question())
                await bot.send_message(chat_id=message.chat.id,
                                       text=question[1], reply_markup=create_keyboard_pass_question())
            db.update_chats_answered_questions(answered_questions=f"{chat[8]} {str(question[0])} ", chat_id=chat[0])


@dp.callback_query_handler(IsInConversationCall(), text="pass_question")
async def on_pass_question_clicked(call: CallbackQuery):
    chat = db.select_chat_by_partner_id(partner1_id=int(call.message.chat.id),
                                        partner2_id=int(call.message.chat.id))
    if variables.openness_levels[chat[3]] > 1:
        if chat[1] == int(call.message.chat.id):
            if chat[9] == 0:
                db.update_partner1_passed_questions(partner1_passed=1, chat_id=chat[0])
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            elif chat[9] == 1:
                db.update_partner1_and_2_passed_questions(partner1_passed=0, partner2_passed=0, chat_id=chat[0])
                await bot.edit_message_text(text="Вы пропустили уже 2 вопроса. Возможно вам не подходит данный уровень"
                                                 "откровенности. Попробуйте начать с предыдущего.",
                                            chat_id=call.message.chat.id,
                                            message_id=call.message.message_id)
                await bot.send_message(chat_id=chat[2], text="Ваш собеседник пропустил уже 2 вопроса. "
                                                             "Возможно вам не подходит данный уровень откровенности. "
                                                             "Попробуйте начать с предыдущего")
                levels = list(variables.openness_levels.keys())
                new_level = levels[variables.openness_levels[chat[3]] - 1]
                db.update_chat_openness(openness=new_level, chat_id=chat[0])
        elif chat[2] == int(call.message.chat.id):
            if chat[9] == 0:
                db.update_partner2_passed_questions(partner2_passed=1, chat_id=chat[0])
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            elif chat[9] == 1:
                db.update_partner1_and_2_passed_questions(partner1_passed=0, partner2_passed=0, chat_id=chat[0])
                await bot.edit_message_text(text="Вы пропустили уже 2 вопроса. Возможно вам не подходит данный уровень"
                                                 "откровенности. Попробуйте начать с предыдущего.",
                                            chat_id=call.message.chat.id,
                                            message_id=call.message.message_id)
                await bot.send_message(chat_id=chat[1], text="Ваш собеседник пропустил уже 2 вопроса. "
                                                             "Возможно вам не подходит данный уровень откровенности. "
                                                             "Попробуйте начать с предыдущего")
                levels = list(variables.openness_levels.keys())
                new_level = levels[variables.openness_levels[chat[3]] - 1]
                db.update_chat_openness(openness=new_level, chat_id=chat[0])
    else:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(IsInConversationCall(), text="ready_lvl_up")
async def on_ready_to_level_up_clicked(call: CallbackQuery):
    chat = db.select_chat_by_partner_id(partner1_id=int(call.message.chat.id),
                                        partner2_id=int(call.message.chat.id))
    if variables.openness_levels[chat[3]] < 5:
        if chat[1] == int(call.message.chat.id):
            if chat[12] == "False":
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Ваш собеседник пока не овтетил готов ли он перейти на новый уровень "
                                                 "откровенности. Как только он ответит мы сообщим Вам.")
                db.update_chat_partner1_ready_to_lvl_up(partner1_ready_to_lvl_up="True", chat_id=chat[0])
            elif chat[12] == "True":
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Вы и Ваш собеседник согласны перейти на новый уровень откровенности.")
                await bot.send_message(chat_id=chat[2],
                                       text="Вы и Ваш собеседник согласны перейти на новый уровень откровенности.")
                levels = list(variables.openness_levels.keys())
                new_level = levels[variables.openness_levels[chat[3]]]
                db.update_chat_openness_and_readiness(openness=new_level, partner1_ready_to_lvl_up="False",
                                                      partner2_ready_to_lvl_up="False", partner1_passed=0,
                                                      partner2_passed=0, chat_id=chat[0])
        elif chat[2] == int(call.message.chat.id):
            if chat[11] == "False":
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Ваш собеседник пока не овтетил готов ли он перейти на новый уровень "
                                                 "откровенности. Как только он ответит мы сообщим Вам.")
                db.update_chat_partner2_ready_to_lvl_up(partner2_ready_to_lvl_up="True", chat_id=chat[0])
            elif chat[11] == "True":
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            text="Вы и Ваш собеседник согласны перейти на новый уровень откровенности.")
                await bot.send_message(chat_id=chat[1],
                                       text="Вы и Ваш собеседник согласны перейти на новый уровень откровенности.")
                levels = list(variables.openness_levels.keys())
                new_level = levels[variables.openness_levels[chat[3]]]
                db.update_chat_openness_and_readiness(openness=new_level, partner1_ready_to_lvl_up="False",
                                                      partner2_ready_to_lvl_up="False", partner1_passed=0,
                                                      partner2_passed=0, chat_id=chat[0])

# @dp.message_handler(IsInConversation(), content_types=types.ContentTypes.CONTACT)
# async def handle_contact_exchange(message: types.Message):
#     chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
#                                         partner2_id=int(message.chat.id))
#     if chat[5] == "False":
#         if chat[1] == int(message.chat.id):
#             db.update_chat_exchange_contacts_partner1(exchange_contacts="True",
#                                                       partner1_phone_number=message.contact.phone_number,
#                                                       chat_id=chat[0])
#         elif chat[2] == int(message.chat.id):
#             db.update_chat_exchange_contacts_partner2(exchange_contacts="True",
#                                                       partner2_phone_number=message.contact.phone_number,
#                                                       chat_id=chat[0])
#         await bot.send_message(chat_id=message.chat.id, text="Бот отправит Вам контакты собеседника когда "
#                                                              "собеседник тоже будет готов обменяться контактами.")
#     elif chat[5] == "True":
#         if chat[1] == int(message.chat.id):
#             db.update_chat_exchange_contacts_partner1(exchange_contacts="True",
#                                                       partner1_phone_number=message.contact.phone_number,
#                                                       chat_id=chat[0])
#             await bot.send_message(chat_id=message.chat.id, text=f"Номер телефона собеседника: {chat[7]}")
#             await bot.send_message(chat_id=chat[2], text=f"Номер телефона собеседника: {message.contact.phone_number}")
#         elif chat[2] == int(message.chat.id):
#             db.update_chat_exchange_contacts_partner2(exchange_contacts="True",
#                                                       partner2_phone_number=message.contact.phone_number,
#                                                       chat_id=chat[0])
#             await bot.send_message(chat_id=message.chat.id, text=f"Номер телефона собеседника: {chat[6]}")
#             await bot.send_message(chat_id=chat[1], text=f"Номер телефона собеседника: {message.contact.phone_number}")
