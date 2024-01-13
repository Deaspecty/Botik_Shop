from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.query_cb import ReceiptCallback, BackCallback
from tgbot.keyboards.user.main import user_main_btns, get_shop_cart_btns
from tgbot.misc.generate_order import show_order
from tgbot.misc.show_product import show_product_function
from tgbot.misc.states.user import ShopCart
from tgbot.misc.delete import remove


async def shop_cart_handler(
        message: Message,
        session: AsyncSession,
        state: FSMContext
):
    data = await state.get_data()
    products = []
    counts = []
    if data.get('shop_cart') is not None:
        for i in data.get('shop_cart').items():
            products.append(int(i[0]))
            counts.append(i[1])

    btns = await get_shop_cart_btns(
        session=session,
        shop_cart=products,
        counts=counts
    )
    await remove(message, 1)
    await message.delete()
    if products:
        await message.answer(
            text="Ваша корзина",
            reply_markup=btns
        )
        await ShopCart.wait_product.set()
    else:
        await message.answer(
            text="В корзине пусто",
            reply_markup=user_main_btns()
        )


async def shop_cart_quantity_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        callback_data: dict,
        state: FSMContext
):
    await show_product_function(callback, session, state, callback_data, 'cart')


async def purchase_shop_cart_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        callback_data: dict,
        state: FSMContext
):
    shop_cart = callback_data.get('shop_cart')
    #date = await state.get_data()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="Прикрепить чек",
        callback_data=ReceiptCallback.new(
            receipt='check',
            action='receipt'
        )
    ))
    markup.add(InlineKeyboardButton(
        text="⬅️Назад",
        callback_data=BackCallback.new(
            level="1_cart",
            action="back"
        )
    ))
    markup.add(InlineKeyboardButton(
        text="⬅️Назад на главную",
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    ))

    await callback.message.edit_text(
        text=await show_order(session=session, shop_cart=eval(shop_cart)),
        reply_markup=markup
    )


async def send_receipt_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        callback_data: dict,
        state: FSMContext
):
    await callback.message.delete()

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="⬅️Назад",
        callback_data=BackCallback.new(
            level="2_cart",
            action="back"
        )
    ))
    markup.add(InlineKeyboardButton(
        text="⬅️Назад на главную",
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    ))
    await callback.message.answer(
        text="Скиньте скриншот чека или pdf",
        reply_markup=markup
    )


async def picture_or_pdf_handler(
        message: Message,
        session: AsyncSession,
        state: FSMContext
):
    pass