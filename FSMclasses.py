from aiogram.dispatcher.filters.state import State, StatesGroup


class sendAnonimMessage(StatesGroup):
    message = State()


class sendAnonimAnswer(StatesGroup):
    answer = State()


class setgreetFSM(StatesGroup):
    greeting = State()

class setnameFSM(StatesGroup):
    newname = State()
    agree = State()