from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from data.variables import admins


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return int(message.chat.id) in admins


class IsAdminCall(BoundFilter):
    async def check(self, call: CallbackQuery) -> bool:
        return int(call.message.chat.id) in admins
