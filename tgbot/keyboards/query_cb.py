from typing import Optional, Union
from aiogram.utils.callback_data import CallbackData


ProductCallback = CallbackData(
    'product', 'product_id', 'action'
)

ShopCartCallback = CallbackData(
    'product', 'product_id', 'count', 'action'
)

OrderCallback = CallbackData(
    'order', 'order_id', 'action'
)

QuantityCallback = CallbackData(
    'quantity', 'turn', 'product_id', 'action'
)

BackCallback = CallbackData(
    'back', 'level', 'action'
)

FAQCallback = CallbackData(
    'FAQ', 'id', 'action'
)

ConfirmCallback = CallbackData(
    'confirm', 'answer', 'action'
)

LanguageCallback = CallbackData(
    'lang', 'lang', 'action'
)

PurchaseCallback = CallbackData(
    'purchase', 'shop_cart', 'action'
)

ReceiptCallback = CallbackData(
    'receipt', 'receipt', 'action'
)


NavigationCallback = CallbackData(
    'navigation', 'by', 'turn', 'count', 'action'
)

