from aiogram.types.message import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.database.user import User
from tgbot.handlers.user.start import start_handler
from tgbot.handlers.user.catalog import choose_product_handler
from tgbot.handlers.user.cart import shop_cart_handler


async def back_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User,
        callback_data: dict,
        state: FSMContext
):
    level = callback_data.get('level')
    if level == '0':
        await callback.message.delete()
        return await start_handler(message=callback.message,
                                   user=user)
    if 'order' in level:
        return await choose_product_handler(
            message=callback.message,
            session=session,
            user=user,
            state=state
        )
    else:
        return await shop_cart_handler(
            message=callback.message,
            session=session,
            state=state,
            user=user
        )


