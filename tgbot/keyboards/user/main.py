from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.database.product import get_all_products, get_product_by_id, get_all_products_by_id
from tgbot.keyboards import generate
from tgbot.keyboards.query_cb import (ProductCallback, BackCallback,
                                      LanguageCallback, QuantityCallback,
                                      ShopCartCallback, PurchaseCallback)
from tgbot.data.locale import Lang


def phone_number_btn():
    markup = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True
    )
    markup.add(
        KeyboardButton("Поделиться телефоном", request_contact=True)
    )
    return markup


def user_main_btns():
    markup = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True
    )

    markup.add(
        "Каталог"
    )
    markup.add(
        "FIQ"
    )
    markup.add(
        "Контакты"
    )
    markup.add(
        "Сменить язык"
    )
    markup.add(
        "Корзина"
    )

    return markup


def get_orders():
    pass


async def get_product_btns(session: AsyncSession,
                           product_id: int,
                           action: str,
                           count: int = 0):
    markup = InlineKeyboardMarkup()
    product = await get_product_by_id(session, product_id)
    btns = {}
    btns['⬅️'] = QuantityCallback.new(
        turn=-1,
        product_id=product_id,
        action=action
    )

    btns[str(count)] = QuantityCallback.new(
        turn='-',
        product_id='-',
        action="-"
    )
    btns['➡️'] = QuantityCallback.new(
        turn=1,
        product_id=product_id,
        action=action
    )
    btns['⬅️Назад'] = BackCallback.new(
        level=f"1_{action}",
        action="back"
    )
    btns['⬅️Назад на главную'] = BackCallback.new(
        level=0,
        action="back"
    )
    order_btns = generate.GenerateMarkupButtons(
        laylout=[3, 1, 1],
        markup=markup,
        keyboards=[
            InlineKeyboardButton(
                text=t,
                callback_data=c
            ) for t, c in btns.items()
        ]
    ).get()
    return order_btns, product


async def get_products_btns(session: AsyncSession):
    markup = InlineKeyboardMarkup()
    products = await get_all_products(session)
    btns = {}
    for product in products:
        btns[product.name] = ProductCallback.new(
            product_id=product.id,
            action="product"
        )
    btns['⬅️Назад'] = BackCallback.new(
            level=0,
            action="back"
    )
    return generate.GenerateMarkupButtons(
        laylout=1,
        markup=markup,
        keyboards=[
            InlineKeyboardButton(
                text=t,
                callback_data=c
            ) for t, c in btns.items()
        ]
    ).get()


async def get_shop_cart_btns(session: AsyncSession,
                             shop_cart: list,
                             counts: list):
    markup = InlineKeyboardMarkup()
    products = await get_all_products_by_id(session, shop_cart)
    btns = {}
    for i, product in enumerate(products):
        btns[f"{product.name}({counts[i]}x)"] = ShopCartCallback.new(
            product_id=product.id,
            count=counts[i],
            action="product"
        )
    btns['🛒Купить'] = PurchaseCallback.new(
        shop_cart=[shop_cart, counts],
        action="purchase"
    )
    btns['⬅️Назад'] = BackCallback.new(
            level=0,
            action="back"
    )
    return generate.GenerateMarkupButtons(
        laylout=1,
        markup=markup,
        keyboards=[
            InlineKeyboardButton(
                text=t,
                callback_data=c
            ) for t, c in btns.items()
        ]
    ).get()


async def get_lang_btns(action: str):
    markup = InlineKeyboardMarkup()
    btns = {}

    btns['Русский'] = LanguageCallback.new(
        lang=Lang.RUS,
        action=action
    )

    btns['Узбекский'] = LanguageCallback.new(
        lang=Lang.UZB,
        action=action
    )

    return generate.GenerateMarkupButtons(
        laylout=1,
        markup=markup,
        keyboards=[
            InlineKeyboardButton(
                text=t,
                callback_data=c
            ) for t, c in btns.items()
        ]
    ).get()

