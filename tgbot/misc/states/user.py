from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    wait_user = State()


class AuthUser(StatesGroup):
    wait_phone = State()
    wait_name = State()
    wait_lang = State()
    wait_region = State()


class Order(StatesGroup):
    #wait_category = State()
    wait_product = State()
    wait_order = State()


class ShopCart(StatesGroup):
    wait_product = State()
    wait_name = State()
    wait_file = State()
    wait_phone = State()
    wait_info = State()


class Locale(StatesGroup):
    wait_user = State()


class CoopState(StatesGroup):
    wait_user = State()
