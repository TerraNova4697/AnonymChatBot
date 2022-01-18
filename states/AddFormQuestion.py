from aiogram.dispatcher.filters.state import StatesGroup, State


class AddFormQuestion(StatesGroup):
    InputQuestion = State()
    QuestionMenu = State()
    NewOption = State()
    DeleteQuestion = State()
