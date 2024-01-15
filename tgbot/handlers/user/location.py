from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message, ContentTypes, ParseMode
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.misc.delete import remove
from tgbot.misc.states.user import Locale, UserState
from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.keyboards.user.main import get_lang_btns, user_main_btns
from tgbot.keyboards.query_cb import BackCallback


async def locale_main_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    await remove(message, 1)
    await message.delete()
    btns = await get_lang_btns('lang_ch')
    btns.add(InlineKeyboardButton(
        text=f"⬅️{LocaleManager.get('Назад', user.lang)}",
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    ))
    await message.answer(
        text="Выберите язык",
        reply_markup=btns
    )
    await Locale.wait_user.set()


async def set_locale_handler(
        callback: CallbackQuery,
        state: FSMContext,
        user: User,
        callback_data: dict
):
    await callback.message.delete()
    await callback.message.answer(LocaleManager.get("Вы сменили язык", user.lang),
                                  reply_markup=user_main_btns(user.lang))
    await UserState.wait_user.set()
