from aiogram.fsm.state import State, StatesGroup


class start(StatesGroup):
    name_surname = State()


class application(StatesGroup):
    topic = State()
    application = State()


class email(StatesGroup):
    email = State()
    password = State()


class email_incoming(StatesGroup):
    email = State()


class ticket(StatesGroup):
    ticket = State()


class false(StatesGroup):
    text = State()
    ticket_user_id = State()


class duplicate_by_ticket(StatesGroup):
    duplicate_by_ticket = State()
