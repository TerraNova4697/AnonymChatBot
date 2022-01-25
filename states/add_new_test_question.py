from aiogram.dispatcher.filters.state import StatesGroup, State


class AddNewQuestion(StatesGroup):
    NewTestQuestionInput = State()
    EditTestQuestion = State()
    AddCorrect = State()
    AddIncorrect = State()
