from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterAdmin(StatesGroup):
    InputName = State()
    InputSurname = State()
