from aiogram.types import CallbackQuery

from filters import IsOwnerCall, IsAdminCall
from loader import dp


@dp.callback_query_handler(IsOwnerCall(), text="sync_bot")
@dp.callback_query_handler(IsAdminCall(), text="sync_bot")
async def sync_bot(call: CallbackQuery):
    await call.answer(text='Синхронизирую бота с гугл-таблицей')
