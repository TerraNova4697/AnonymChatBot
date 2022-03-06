from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from loader import db


class IsInConversation(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                            partner2_id=int(message.chat.id))
        if chat is not None and message.text != "Получить вопрос":
            if chat[4] == 'Conversation':
                return True
        else:
            return False


class IsInConversationCall(BoundFilter):
    async def check(self, call: CallbackQuery) -> bool:
        chat = db.select_chat_by_partner_id(partner1_id=int(call.message.chat.id),
                                            partner2_id=int(call.message.chat.id))
        if chat is not None and call.message.text != "Получить вопрос":
            if chat[4] == 'Conversation':
                return True
        else:
            return False


class IsInConversationGetQuestion(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                            partner2_id=int(message.chat.id))
        if chat is not None and message.text == "Получить вопрос":
            if chat[4] == 'Conversation':
                return True
        else:
            return False
