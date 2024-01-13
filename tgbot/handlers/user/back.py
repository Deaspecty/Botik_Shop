from aiogram.types.message import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.user.main import user_main_btns, get_products_btns, get_product_btns
from tgbot.handlers.user.start import start_handler
from tgbot.handlers.user.catalog import choose_product_handler
from tgbot.handlers.user.cart import shop_cart_handler
from tgbot.misc.states.user import Order


async def back_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        callback_data: dict,
        state: FSMContext
):
    level = callback_data.get('level')
    if level == '0':
        await callback.message.delete()
        return await start_handler(message=callback.message)
    if 'order' in level:
        return await choose_product_handler(
            message=callback.message,
            session=session)
    else:
        return await shop_cart_handler(
            message=callback.message,
            session=session,
            state=state
        )


