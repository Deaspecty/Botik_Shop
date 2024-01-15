from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message, ContentTypes, ParseMode
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.database.user import User
from tgbot.handlers.user.catalog import choose_product_handler
from tgbot.handlers.user.cart import shop_cart_handler


async def navigation(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User,
        state: FSMContext,
        callback_data: dict
):
    #data = await state.get_data()
    loc = int(callback_data['turn'])
    count = int(callback_data['count'])
    if loc > count - 1:
        loc = 0
    elif loc < 0:
        loc = (count - (count % 5))
    if callback_data['by'] == 'orders':
        await state.update_data(loc=loc)
        await choose_product_handler(
            message=callback.message,
            session=session,
            user=user,
            state=state
        )
    elif callback_data['by'] == 'shop_cart':
        await state.update_data(loc_cart=loc)
        await shop_cart_handler(
            message=callback.message,
            session=session,
            user=user,
            state=state
        )
