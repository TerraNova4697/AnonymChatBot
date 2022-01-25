from aiogram.dispatcher.filters.state import StatesGroup, State


class EditTestQuestion(StatesGroup):
    Edit = State()
    Delete = State()
    ChangeText = State()
