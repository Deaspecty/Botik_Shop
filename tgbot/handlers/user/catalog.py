from aiogram.types.message import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.handlers.user.cart import shop_cart_handler
from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.keyboards.user.main import (user_main_btns, get_products_btns,
                                       get_category, get_marketplace)
from tgbot.misc.show_product import show_product_function
from tgbot.misc.states.user import Order
from tgbot.misc.delete import remove


async def get_marketplace_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    data = await state.get_data()
    btns = await get_marketplace(
        lang=user.lang,
        region=user.region
    )
    await message.delete()
    #await remove(message, 1)
    if btns:
        await message.answer(
            text=LocaleManager.get("Магазина", user.lang),
            reply_markup=btns
        )


async def choose_category_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    data = await state.get_data()
    btns = await get_category(
        session=session,
        lang=user.lang,
        shop_cart=data.get('shop_cart')
    )
    await message.delete()
    #await remove(message, 1)
    if btns:
        await message.answer(
            text=LocaleManager.get("Выберите товар", user.lang),
            reply_markup=btns
        )
    await Order.wait_product.set()


async def choose_product_handler(
        callback: CallbackQuery,
        #message: Message,
        session: AsyncSession,
        user: User,
        callback_data: dict,
        state: FSMContext
):
    data = await state.get_data()
    loc = data.get('loc')
    sub_str = callback_data.get('category_sub')
    btns = await get_products_btns(
        session=session,
        lang=user.lang,
        shop_cart=data.get('shop_cart'),
        loc=int(loc) if loc is not None else 0,
        sub_str=sub_str
    )
    await remove(callback.message, 1)
    try:
        await callback.message.delete()
    except Exception:
        pass
    if btns:
        await callback.message.answer(
            text=LocaleManager.get("Выберите товар", user.lang),
            reply_markup=btns
        )
        #await Order.wait_product.set()
    else:
        await callback.message.answer(
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
