from aiogram.types.message import Message

from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.keyboards.user.main import user_main_btns
from tgbot.misc.states.user import UserState


async def start_handler(
        message: Message,
        user: User
):
    await message.answer(
        text=LocaleManager.get("Добро пожаловать", user.lang),
        reply_markup=user_main_btns(user.lang)
    )
    await UserState.wait_user.set()
