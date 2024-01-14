from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    wait_user = State()


class AuthUser(StatesGroup):
    wait_phone = State()
    wait_name = State()
    wait_lang = State()


class Order(StatesGroup):
    wait_product = State()
    wait_order = State()


class ShopCart(StatesGroup):
    wait_product = State()
    wait_file = State()
