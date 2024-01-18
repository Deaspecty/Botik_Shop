from aiogram.types.message import Message

from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.keyboards.user.main import user_main_btns
from tgbot.misc.states.user import UserState
from tgbot.misc.delete import remove


async def start_handler(
        message: Message,
        user: User
):
    await remove(message, 1)
    text = '''Добро пожаловать в магазин нашей компании
Для выбора продукции перейдите в Каталог в главном меню ниже
'''
    await message.answer(
        text=LocaleManager.get(text, user.lang) + " ⬇️",
        reply_markup=user_main_btns(user.lang)
    )
    await UserState.wait_user.set()
