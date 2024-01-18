from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message, ContentTypes, ParseMode
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.misc.delete import remove
from tgbot.misc.states.user import UserState
from tgbot.data.locale import LocaleManager
from tgbot.data.FAQ_info import faq_text
from tgbot.models.database.user import User
from tgbot.keyboards.query_cb import BackCallback
from tgbot.keyboards.user.faq import get_faq_btns


async def faq_main_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    markup = await get_faq_btns('0', user.lang)
    markup.add(InlineKeyboardButton(
        text=f"⬅️{LocaleManager.get('Назад', user.lang)}",
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    ))
    await remove(message, 1)
    await message.delete()
    await message.answer(LocaleManager.get('FAQ', user.lang),
                         reply_markup=markup)
    await UserState.wait_user.set()


async def get_faq_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User,
        callback_data: dict
):
    id_loc = callback_data['id']
    markup = await get_faq_btns(id_loc, user.lang)
    markup.add(InlineKeyboardButton(
        text=f"⬅️{LocaleManager.get('Назад', user.lang)}",
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    ))
    await callback.message.edit_text(
        text=LocaleManager.get(faq_text.get(id_loc), user.lang),
        reply_markup=markup)
