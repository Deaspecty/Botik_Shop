from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.filters import OrFilter

from tgbot.misc.states.user import Order, ShopCart, Locale
from tgbot.keyboards.query_cb import (QuantityCallback, ProductCallback,
                                      ShopCartCallback, BackCallback, PurchaseCallback,
                                      ReceiptCallback, LanguageCallback, NavigationCallback)
from tgbot.handlers.user.catalog import (choose_product_handler,
                                         order_quantity_handler,
                                         get_shop_cart_handler)
from tgbot.handlers.user.cart import (shop_cart_handler, shop_cart_quantity_handler,
                                      purchase_shop_cart_handler, get_picture_or_pdf_handler,
                                      clear_shop_cart_handler, send_receipt_handler,
                                      remove_product_cart_handler, save_phone_handler)
from tgbot.handlers.user.faq import faq_main_handler
from tgbot.handlers.user.contacts import contacts_main_handler
from tgbot.handlers.user.back import back_handler
from tgbot.handlers.user.location import locale_main_handler, set_locale_handler
from tgbot.handlers.user.navigation import navigation


def register_client_function(dp: Dispatcher):
    register_catalog_function(dp)
    register_cart_function(dp)
    register_back_function(dp)
    register_local_function(dp)
    register_contacts_function(dp)
    register_faq_function(dp)


def register_catalog_function(dp: Dispatcher):
    dp.register_message_handler(
        choose_product_handler,
        text='Каталог',
        state="*"
    )

    dp.register_callback_query_handler(
        order_quantity_handler,
        ProductCallback.filter(action="product"),
        state=Order.wait_product
    )

    dp.register_callback_query_handler(
        order_quantity_handler,
        QuantityCallback.filter(action="order"),
        state=Order.wait_product
    )

    dp.register_callback_query_handler(
        get_shop_cart_handler,
        ProductCallback.filter(action="shop_cart"),
        state=Order.wait_product
    )

    dp.register_callback_query_handler(
        get_shop_cart_handler,
        QuantityCallback.filter(action="shop_cart"),
        state=Order.wait_product
    )

    dp.register_callback_query_handler(
        navigation,
        NavigationCallback.filter(action="navigation"),
        state="*"
    )


def register_cart_function(dp: Dispatcher):
    dp.register_message_handler(
        shop_cart_handler,
        text='Корзина',
        state="*"
    )

    dp.register_callback_query_handler(
        shop_cart_quantity_handler,
        ShopCartCallback.filter(action="product"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        get_shop_cart_handler,
        QuantityCallback.filter(action="shop_cart"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        shop_cart_quantity_handler,
        QuantityCallback.filter(action="cart"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        purchase_shop_cart_handler,
        PurchaseCallback.filter(action="purchase"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        clear_shop_cart_handler,
        PurchaseCallback.filter(action="clear_cart"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        remove_product_cart_handler,
        PurchaseCallback.filter(action="remove"),
        state=ShopCart.wait_product
    )

    dp.register_callback_query_handler(
        send_receipt_handler,
        ReceiptCallback.filter(action="receipt"),
        state=ShopCart.wait_product
    )

    dp.register_message_handler(
        save_phone_handler,
        content_types=types.ContentType.CONTACT,
        state=ShopCart.wait_phone
    )

    dp.register_message_handler(
        get_picture_or_pdf_handler,
        content_types=types.ContentTypes.ANY,
        state=ShopCart.wait_file
    )


def register_back_function(dp: Dispatcher):
    dp.register_callback_query_handler(
        back_handler,
        BackCallback.filter(action="back"),
        state="*"
    )


def register_faq_function(dp: Dispatcher):
    dp.register_message_handler(
        faq_main_handler,
        text='FAQ',
        state="*"
    )


def register_contacts_function(dp: Dispatcher):
    dp.register_message_handler(
        contacts_main_handler,
        text='Контакты',
        state="*"
    )


def register_local_function(dp: Dispatcher):
    dp.register_message_handler(
        locale_main_handler,
        text='Сменить язык',
        state="*"
    )

    dp.register_callback_query_handler(
        set_locale_handler,
        LanguageCallback.filter(action='lang_ch'),
        state=Locale.wait_user
    )
