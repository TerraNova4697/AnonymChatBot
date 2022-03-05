from aiogram import types
from aiogram.types import ContentType

from filters import IsInConversation
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
