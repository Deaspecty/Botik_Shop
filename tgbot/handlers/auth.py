from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types.message import Message, ContentType
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.misc.states.user import AuthUser, UserState
from tgbot.keyboards.user.main import phone_number_btn


async def phone_handler(
        m: Message,
        user: User,
        state: State,
        state_date: FSMContext = None
):
    text = "Поделитесь номером телефона для авторизации"
    if not (lang := user.lang):
        data = await state_date.get_data()
        lang = data['lang']

    await m.answer(
        text=LocaleManager.get(text, lang),
        reply_markup=phone_number_btn(lang)
    )

    await state.set()


async def auth_user_handler(
        message: Message,
        user: User,
        state: FSMContext
):
    await phone_handler(message, user, UserState.wait_user)
