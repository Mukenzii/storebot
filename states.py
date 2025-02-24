from telebot.handler_backends import State, StatesGroup


class RegisterStates(StatesGroup):
    full_name = State()
    contact = State()
    birthdate = State()
    submit = State()

class CardState(StatesGroup):
    card = State()

class ProductState(StatesGroup):
    product_name = State()
    price = State()
    image = State()
    link = State()
    category = State()


