from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import LocaleManager
from tgbot.models.database.product import get_all_products, get_product_by_id, get_all_products_by_id
from tgbot.keyboards import generate
from tgbot.keyboards.query_cb import (ProductCallback, BackCallback,
                                      LanguageCallback, QuantityCallback,
                                      ShopCartCallback, PurchaseCallback)
from tgbot.data.locale import Lang


def phone_number_btn(lang):
    markup = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True
    )
    markup.add(
        KeyboardButton(LocaleManager.get("Поделиться телефоном", lang), request_contact=True)
    )
    return markup


def user_main_btns(lang):
    markup = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True
    )
    btns = [LocaleManager.get("Каталог", lang),
            LocaleManager.get("FAQ", lang),
            LocaleManager.get("Контакты", lang),
            LocaleManager.get("Сменить язык", lang),
            LocaleManager.get("Корзина", lang)]
    for btn in btns:
        markup.add(
            btn
        )

    return markup


def get_orders():
    pass


async def get_product_btns(session: AsyncSession,
                           product_id: int,
                           action: str,
                           lang: str,
                           count: int = 0):
    markup = InlineKeyboardMarkup()
    product = await get_product_by_id(session, product_id)
    btns = {'⬅️': QuantityCallback.new(
        turn=-1,
        product_id=product_id,
        action=action
    ), str(count): QuantityCallback.new(
        turn='-',
        product_id='-',
        action="-"
    ), '➡️': QuantityCallback.new(
        turn=1,
        product_id=product_id,
        action=action
    ), f'⬅️{LocaleManager.get("Назад", lang)}': BackCallback.new(
        level=f"1_{action}",
        action="back"
    ), f'⬅️{LocaleManager.get("Назад на главную", lang)}': BackCallback.new(
        level=0,
        action="back"
    )}

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


async def get_products_btns(session: AsyncSession,
                            lang: str):
    markup = InlineKeyboardMarkup()
    products = await get_all_products(session)
    btns = {}
    for product in products:
        btns[LocaleManager.get(product.name, lang)] = ProductCallback.new(
            product_id=product.id,
            action="product"
        )
    btns[f'⬅️{LocaleManager.get("Назад", lang)}'] = BackCallback.new(
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
                             counts: list,
                             lang: str):
    markup = InlineKeyboardMarkup()
    products = await get_all_products_by_id(session, shop_cart)
    btns = {}
    for i, product in enumerate(products):
        btns[f"{LocaleManager.get(product.name, lang)}"] = ShopCartCallback.new(
            product_id=product.id,
            count=counts[i],
            action="product"
        )
        btns[f"🗑{i + 1}({counts[i]} шт)"] = PurchaseCallback.new(
            shop_cart=product.id,
            action="remove"
        )
    btns[f'🛒{LocaleManager.get("Купить", lang)}'] = PurchaseCallback.new(
        shop_cart=[shop_cart, counts],
        action="purchase"
    )
    btns[f'🧹{LocaleManager.get("Очистить корзину", lang)}'] = PurchaseCallback.new(
        shop_cart=[shop_cart, counts],
        action="clear_cart"
    )
    btns[f'⬅️{LocaleManager.get("Назад", lang)}'] = BackCallback.new(
            level=0,
            action="back"
    )
    return generate.GenerateMarkupButtons(
        laylout=[2] * len(counts) + [1] * 3,
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
    btns = {'Русский': LanguageCallback.new(
        lang=Lang.RUS,
        action=action
    ), 'Узбекский': LanguageCallback.new(
        lang=Lang.UZB,
        action=action
    )}

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


async def get_back_btns(lang: str):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text=f"⬅️{LocaleManager.get('Назад', lang)}",
        callback_data=BackCallback.new(
            level="2_cart",
            action="back"
        )
    ))
    markup.add(InlineKeyboardButton(
        text=f"⬅️{LocaleManager.get('Назад на главную', lang)}",
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    ))
    return markup
