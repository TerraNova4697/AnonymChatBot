from aiogram.dispatcher.filters.state import StatesGroup, State


class EditQuestion(StatesGroup):
    EditText = State()
    EditCategory = State()
