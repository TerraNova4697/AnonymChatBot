from aiogram.dispatcher.filters.state import StatesGroup, State


class FillInForms(StatesGroup):
    InputUsername = State()
    FillInForm = State()
    ChooseImportant = State()
    WriteToDB = State()
    ChoosePartnersValue = State()
