from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery

from data.variables import owner


class IsOwner(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return str(message.chat.id) in owner


class IsOwnerCall(BoundFilter):
    async def check(self, call: CallbackQuery) -> bool:
        return str(call.message.chat.id) in owner


class IsNotOwner(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return str(message.chat.id) not in owner
