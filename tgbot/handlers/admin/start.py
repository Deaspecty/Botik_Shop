from aiogram.types.message import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.user.main import user_main_btns
from tgbot.misc.states.user import UserState


async def start_handler(
        message: Message
):
    await message.answer(
        text="Добро пожаловать админ"
    )

