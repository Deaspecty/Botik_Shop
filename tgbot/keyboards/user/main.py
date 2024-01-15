from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import LocaleManager
from tgbot.models.database.product import get_all_products, get_product_by_id, get_all_products_by_id
from tgbot.keyboards import generate
from tgbot.keyboards.query_cb import (ProductCallback, BackCallback,
                                      LanguageCallback, QuantityCallback,
                                      ShopCartCallback, PurchaseCallback,
                                      NavigationCallback)
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
            LocaleManager.get("Корзина", lang),
            LocaleManager.get("FAQ", lang),
            LocaleManager.get("Контакты", lang),
            LocaleManager.get("Сменить язык", lang)]
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
                           shop_cart: dict,
                           count: int = 0):
    markup = InlineKeyboardMarkup()
    product = await get_product_by_id(session, product_id)
    laylout = [3, 1]
    btns = {'➖': QuantityCallback.new(
        turn=-1,
        product_id=product_id,
        action=action
    ), str(count): QuantityCallback.new(
        turn='-',
        product_id='-',
        action="-"
    ), '➕': QuantityCallback.new(
        turn=1,
        product_id=product_id,
        action=action
    ), f'⬅️{LocaleManager.get("Назад", lang)}': BackCallback.new(
        level=f"1_{action}",
        action="back"
    )
        #, f'⬅️{LocaleManager.get("Назад на главную", lang)}': BackCallback.new(
        #level=0,
        #action="back")
    }
    if shop_cart:
        laylout.append(1)
        btns[f'🛒{LocaleManager.get("Корзина", lang)}'] = QuantityCallback.new(
            turn='-',
            product_id='-',
            action="shop_cart"
        )
    order_btns = generate.GenerateMarkupButtons(
        laylout=laylout,
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
                            lang: str,
                            shop_cart: dict,
                            loc: int):
    markup = InlineKeyboardMarkup()
    products = await get_all_products(session)
    btns = {}
    layout = []
    for i, product in enumerate(products[loc:]):
        if i == 5:
            break
        btns[LocaleManager.get(product.name, lang)] = ProductCallback.new(
            product_id=product.id,
            action="product"
        )
        layout += [1]
    if shop_cart:
        btns[f'🛒{LocaleManager.get("Корзина", lang)}'] = ProductCallback.new(
            product_id="-",
            action="shop_cart"
        )
        layout += [1]

    if len(products) > 5:
        btns["⬅️"] = NavigationCallback.new(
            by="orders",
            turn=loc - 5,
            count=len(products),
            action="navigation"
            )
        btns["➡️"] = NavigationCallback.new(
            by="orders",
            turn=loc + 5,
            count=len(products),
            action="navigation"
        )
        layout += [2]
    btns[f'⬅️{LocaleManager.get("Назад", lang)}'] = BackCallback.new(
            level=0,
            action="back"
    )
    layout += [1]

    return generate.GenerateMarkupButtons(
        laylout=layout,
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
                             lang: str,
                             loc: int):
    markup = InlineKeyboardMarkup()
    products = await get_all_products_by_id(session, shop_cart)
    btns = {}
    layout = []
    for i, product in enumerate(products[loc:]):
        if i == 5:
            break
        btns[f"{LocaleManager.get(product.name, lang)} (x {counts[i]})"] = ShopCartCallback.new(
            product_id=product.id,
            count=counts[i],
            action="product"
        )
        btns[f"🗑{i + 1}"] = PurchaseCallback.new(
            shop_cart=product.id,
            action="remove"
        )
        layout += [2]
    if len(products) > 5:
        btns["⬅️"] = NavigationCallback.new(
            by="shop_cart",
            turn=loc - 5,
            count=len(products),
            action="navigation"
        )
        btns["➡️"] = NavigationCallback.new(
            by="shop_cart",
            turn=loc + 5,
            count=len(products),
            action="navigation"
        )
        layout = layout + [2]
    btns[f'🛒{LocaleManager.get("Купить", lang)}'] = PurchaseCallback.new(
        shop_cart="-",
        action="purchase"
    )
    btns[f'🧹{LocaleManager.get("Очистить корзину", lang)}'] = PurchaseCallback.new(
        shop_cart="-",
        action="clear_cart"
    )
    btns[f'⬅️{LocaleManager.get("Назад", lang)}'] = BackCallback.new(
            level=0,
            action="back"
    )
    layout += [1, 1, 1]
    return generate.GenerateMarkupButtons(
        laylout=layout,
        markup=markup,
        keyboards=[
            InlineKeyboardButton(
                text=t.replace(t[-1], "") if '🗑' in t else t,
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
