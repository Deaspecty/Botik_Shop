from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import LocaleManager
from tgbot.models.database.product import get_all_products, get_product_by_id, get_all_products_by_id
from tgbot.keyboards import generate
from tgbot.keyboards.query_cb import (ProductCallback, BackCallback,
                                      LanguageCallback, QuantityCallback,
                                      ShopCartCallback, PurchaseCallback,
                                      NavigationCallback, CategoryCallback)
from tgbot.data.locale import Lang


def phone_number_btn(lang):
    markup = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True
    )
    markup.add(
        KeyboardButton(LocaleManager.get("Поделиться номером", lang), request_contact=True)
    )
    return markup


def user_main_btns(lang):
    markup = ReplyKeyboardMarkup(
        row_width=2,
        resize_keyboard=True
    )
    btns = [LocaleManager.get("Каталог", lang),
            LocaleManager.get("Купить на маркетплейсе", lang),
            LocaleManager.get("Корзина", lang),
            LocaleManager.get("FAQ", lang),
            LocaleManager.get("Контакты", lang),
            LocaleManager.get("Сменить язык", lang) + " 🇰🇿🇷🇺🇺🇿",
            LocaleManager.get("Сменить локацию", lang) + " 🇰🇿🇷🇺🇺🇿",
            LocaleManager.get("Сотрудничество", lang)]
    for btn in btns:
        markup.add(
            btn
        )

    return markup


async def get_marketplace(lang, region):
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton('Kaspi', url='https://kaspi.kz/shop/info/merchant/17508832/address-tab/?merchantId=17508832&ref=shared_lin')
    btn2 = InlineKeyboardButton('Ozone', url='https://ozon.ru/t/byp0L6q')
    btn3 = InlineKeyboardButton(LocaleManager.get("Wildberries (скоро)", lang),
                                callback_data="test")
    btn4 = InlineKeyboardButton(LocaleManager.get("Я.Маркет (скоро)", lang),
                                callback_data="test")
    btn5 = InlineKeyboardButton(LocaleManager.get("Uzum (скоро)", lang),
                                callback_data="test")
    btn6 = InlineKeyboardButton(
        text="⬅️" + LocaleManager.get("Назад", lang),
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    )
    if region == 'Kazakhstan':
        markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    if region == 'Russia':
        markup.add(btn4)
    if region == 'Uzbekistan':
        markup.add(btn5)
    markup.add(btn6)
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
    btns[f'⬅️{LocaleManager.get("Назад", lang)}'] = BackCallback.new(
        level=f"1_{action}",
        action="back"
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


async def get_category(
        session: AsyncSession,
        lang: str,
        shop_cart: dict
):
    markup = InlineKeyboardMarkup()
    btns = {LocaleManager.get("Ederra Lab 01 шампунь", lang): CategoryCallback.new(
        category_sub="Ederra Lab 01 шампунь",
        action="category"
    ), "Ederra Lab 01 Sulfate Free": CategoryCallback.new(
        category_sub="Sulfate Free",
        action="category"
    ), "Ederra Lab 02 Moisture": CategoryCallback.new(
        category_sub="02 Moisture",
        action="category"
    )}
    products = await get_all_products(session)
    for i, product in enumerate(products):
        if i == 5:
            break
        if "Ederra Lab 03" in product.name:
            btns[LocaleManager.get(product.name, lang)] = ProductCallback.new(
                product_id=product.id,
                action="product"
            )
    if shop_cart:
        btns[f'🛒{LocaleManager.get("Корзина", lang)}'] = QuantityCallback.new(
            turn='-',
            product_id='-',
            action="shop_cart"
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


async def get_products_btns(session: AsyncSession,
                            lang: str,
                            shop_cart: dict,
                            loc: int,
                            sub_str: str):
    markup = InlineKeyboardMarkup()
    products = await get_all_products(session)
    btns = {}
    layout = []
    #products[loc:]
    for i, product in enumerate(products):
        #if i == 5:
        #    break
        if sub_str.lower() in product.name.lower():
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

    if len(layout) > 5:
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
            level="category",
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


async def get_lang_btns(action: str,
                        lang: str = "rus"):
    markup = InlineKeyboardMarkup()
    btns = {'Қазақша' + " 🇰🇿": LanguageCallback.new(
        lang=Lang.KAZ,
        action=action
    ), 'Русский' + " 🇷🇺": LanguageCallback.new(
        lang=Lang.RUS,
        action=action
    ), "O'zbek" + " 🇺🇿": LanguageCallback.new(
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


async def region_btns(action: str,
                      lang: str = "rus"):
    markup = InlineKeyboardMarkup()
    btns = {LocaleManager.get('Казахстан', lang) + " 🇰🇿": LanguageCallback.new(
        lang="Kazakhstan",
        action=action
    ), LocaleManager.get('Россия', lang) + " 🇷🇺": LanguageCallback.new(
        lang="Russia",
        action=action
    ), LocaleManager.get('Узбекистан', lang) + "🇺🇿": LanguageCallback.new(
        lang="Uzbekistan",
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

