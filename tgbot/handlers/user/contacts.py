from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message, ContentTypes, ParseMode
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.misc.delete import remove
from tgbot.misc.states.user import UserState
from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.keyboards.query_cb import BackCallback


async def contacts_main_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text=f"⬅️{LocaleManager.get('Назад', user.lang)}",
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    ))
    #await remove(message, 1)
    await message.delete()
    text = '''Свяжитесь с нами по номеру: +7 708 609 6107'''
    await message.answer(
        text=LocaleManager.get(text, user.lang),
        reply_markup=markup)
    await UserState.wait_user.set()
