from aiogram.types.message import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.handlers.user.cart import shop_cart_handler
from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.keyboards.user.main import user_main_btns, get_products_btns
from tgbot.misc.show_product import show_product_function
from tgbot.misc.states.user import Order
from tgbot.misc.delete import remove


async def choose_product_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    data = await state.get_data()
    loc = data.get('loc')
    btns = await get_products_btns(
        session=session,
        lang=user.lang,
        shop_cart=data.get('shop_cart'),
        loc=int(loc) if loc is not None else 0
    )
    await remove(message, 1)
    await message.delete()
    if btns:
        await message.answer(
            text=LocaleManager.get("Выберите товар", user.lang),
            reply_markup=btns
        )
        await Order.wait_product.set()
    else:
        await message.answer(
            text=LocaleManager.get("Нет товаров в наличи", user.lang),
            reply_markup=user_main_btns(user.lang)
        )


async def order_quantity_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User,
        callback_data: dict,
        state: FSMContext
):
    await show_product_function(callback, session, state, callback_data, user, 'order')


async def get_shop_cart_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User,
        callback_data: dict,
        state: FSMContext
):
    await shop_cart_handler(message=callback.message,
                            session=session,
                            user=user,
                            state=state)
