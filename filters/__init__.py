from aiogram import Dispatcher

from loader import dp
# from .is_admin import AdminFilter
from .is_owner import IsOwner, IsOwnerCall, IsNotOwner
from .is_admin import IsAdmin, IsAdminCall


if __name__ == "filters":
    # dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsOwner)
    dp.filters_factory.bind(IsOwnerCall)
    dp.filters_factory.bind(IsNotOwner)
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsAdminCall)
