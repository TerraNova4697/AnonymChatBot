from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class IsInConversation(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        chat = db.select_chat_by_partner_id(partner1_id=int(message.chat.id),
                                            partner2_id=int(message.chat.id))
        if chat is not None:
            if chat[4] == 'Conversation':
                return True
        else:
            return False
