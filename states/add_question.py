from aiogram.dispatcher.filters.state import StatesGroup, State


class AddQuestion(StatesGroup):
    InputQuestion = State()
    InputOpenness = State()
    InputCategory = State()

