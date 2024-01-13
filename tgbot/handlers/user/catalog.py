from aiogram.types.message import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.user.main import user_main_btns, get_products_btns
from tgbot.misc.show_product import show_product_function
from tgbot.misc.states.user import Order
from tgbot.misc.delete import remove


async def choose_product_handler(
        message: Message,
        session: AsyncSession
):
    btns = await get_products_btns(
        session=session
    )
    await remove(message, 1)
    await message.delete()
    if btns:
        await message.answer(
            text="Выберите товар",
            reply_markup=btns
        )
        await Order.wait_product.set()
    else:
        await message.answer(
            text="Нет товаров в наличи",
            reply_markup=user_main_btns()
        )


async def order_quantity_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        callback_data: dict,
        state: FSMContext
):
    await show_product_function(callback, session, state, callback_data, 'order')
