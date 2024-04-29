from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.filters import OrFilter

from tgbot.misc.states.user import Order, ShopCart, Locale, UserState, CoopState
from tgbot.keyboards import query_cb
from tgbot.handlers.user.catalog import (choose_product_handler,
                                         order_quantity_handler,
                                         get_shop_cart_handler,
                                         choose_category_handler,
                                         get_marketplace_handler)
from tgbot.handlers.user import cart
from tgbot.handlers.user.faq import faq_main_handler, get_faq_handler
from tgbot.handlers.user.coop import get_questionnaire_handler, coop_main_handler, confirm_handler
from tgbot.handlers.user.contacts import contacts_main_handler
from tgbot.handlers.user.back import back_handler
from tgbot.handlers.user.location import (locale_main_handler, set_locale_handler,
                                          set_region_handler, region_main_handler)
from tgbot.handlers.user.navigation import navigation
from tgbot.filters.text import TextKeyboardFilter


def register_client_function(dp: Dispatcher):
    register_catalog_function(dp)
    register_cart_function(dp)
    register_back_function(dp)
    register_local_function(dp)
    register_contacts_function(dp)
    register_faq_function(dp)
    register_coop_function(dp)
    register_market_function(dp)
    register_location_function(dp)


def register_market_function(dp: Dispatcher):
    dp.register_message_handler(
        get_marketplace_handler,
        TextKeyboardFilter(text=['Купить на маркетплейсе']),
        state="*"
    )


def register_catalog_function(dp: Dispatcher):
    dp.register_message_handler(
        choose_category_handler,
        TextKeyboardFilter(text=['Каталог']),
        state="*"
    )

    dp.register_callback_query_handler(
        choose_product_handler,
        query_cb.CategoryCallback.filter(action="category"),
        state=Order.wait_product
    )

    dp.register_callback_query_handler(
        order_quantity_handler,
        query_cb.ProductCallback.filter(action="product"),
        state=Order.wait_product
    )

    dp.register_callback_query_handler(
        order_quantity_handler,
        query_cb.QuantityCallback.filter(action="order"),
        state=Order.wait_product
    )

    dp.register_callback_query_handler(
        get_shop_cart_handler,
        query_cb.ProductCallback.filter(action="shop_cart"),
        state=Order.wait_product
    )

    dp.register_callback_query_handler(
        get_shop_cart_handler,
        query_cb.QuantityCallback.filter(action="shop_cart"),
        state=Order.wait_product
    )

    dp.register_callback_query_handler(
        navigation,
        query_cb.NavigationCallback.filter(action="navigation"),
        state="*"
    )


def register_cart_function(dp: Dispatcher):
    dp.register_message_handler(
        cart.shop_cart_handler,
        TextKeyboardFilter(text=['Корзина']),
        state="*"
    )

    dp.register_callback_query_handler(
        cart.shop_cart_quantity_handler,
        query_cb.ShopCartCallback.filter(action="product"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        get_shop_cart_handler,
        query_cb.QuantityCallback.filter(action="shop_cart"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        cart.shop_cart_quantity_handler,
        query_cb.QuantityCallback.filter(action="cart"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        cart.purchase_shop_cart_handler,
        query_cb.PurchaseCallback.filter(action="purchase"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        cart.clear_shop_cart_handler,
        query_cb.PurchaseCallback.filter(action="clear_cart"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        cart.remove_product_cart_handler,
        query_cb.PurchaseCallback.filter(action="remove"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        cart.send_receipt_handler,
        query_cb.ReceiptCallback.filter(action="receipt"),
        state=ShopCart.wait_product
    )

    dp.register_message_handler(
        cart.save_phone_handler,
        content_types=types.ContentType.CONTACT,
        state=ShopCart.wait_phone
    )

    dp.register_message_handler(
        cart.save_name_handler,
        state=ShopCart.wait_name
    )

    dp.register_message_handler(
        cart.get_picture_or_pdf_handler,
        content_types=types.ContentTypes.ANY,
        state=ShopCart.wait_file
    )

    dp.register_message_handler(
        cart.get_info_handler,
        state=ShopCart.wait_info
    )


def register_back_function(dp: Dispatcher):
    dp.register_callback_query_handler(
        back_handler,
        query_cb.BackCallback.filter(action="back"),
        state="*"
    )


def register_faq_function(dp: Dispatcher):
    dp.register_message_handler(
        faq_main_handler,
        TextKeyboardFilter(text=['FAQ']),
        state="*"
    )

    dp.register_callback_query_handler(
        get_faq_handler,
        query_cb.FAQCallback.filter(action="faq"),
        state=UserState.wait_user
    )


def register_coop_function(dp: Dispatcher):
    dp.register_message_handler(
        coop_main_handler,
        TextKeyboardFilter(text=['Сотрудничество']),
        state="*"
    )

    dp.register_message_handler(
        get_questionnaire_handler,
        state=CoopState.wait_user
    )

    dp.register_callback_query_handler(
        confirm_handler,
        query_cb.ConfirmCallback.filter(action="coop"),
        state=CoopState.wait_user
    )


def register_contacts_function(dp: Dispatcher):
    dp.register_message_handler(
        contacts_main_handler,
        TextKeyboardFilter(text=['Контакты']),
        state="*"
    )


def register_local_function(dp: Dispatcher):
    dp.register_message_handler(
        locale_main_handler,
        TextKeyboardFilter(text=['Сменить язык ' + "🇰🇿🇷🇺"]),
        state="*"
    )

    dp.register_callback_query_handler(
        set_locale_handler,
        query_cb.LanguageCallback.filter(action='lang_ch'),
        state=Locale.wait_user
    )


def register_location_function(dp: Dispatcher):
    dp.register_message_handler(
        region_main_handler,
        TextKeyboardFilter(text=['Сменить локацию ' + "🇰🇿🇷🇺"]),
        state="*"
    )

    dp.register_callback_query_handler(
        set_region_handler,
        query_cb.LanguageCallback.filter(action='region_ch'),
        state=Locale.wait_user
    )
