from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types.message import Message, ContentType
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.database.user import User
from tgbot.misc.states.user import AuthUser, UserState
from tgbot.keyboards.user.main import phone_number_btn


async def phone_handler(
        m: Message,
        state: State
):
    text = "Поделитесь номером телефона для авторизации"

    await m.answer(
        text=text, reply_markup=phone_number_btn()
    )

    await state.set()


async def auth_user_handler(
        message: Message,
        state: FSMContext
):
    await phone_handler(message, UserState.wait_user)
