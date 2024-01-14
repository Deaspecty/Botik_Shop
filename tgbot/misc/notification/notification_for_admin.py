from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import LocaleManager
from tgbot.models.database.product import get_all_products_by_id
from tgbot.models.database.user import User
from tgbot.models.database.order import Order, OrderItem


async def generate_admin_notification(
        session: AsyncSession,
        user: User,
        shop_cart: dict,
):

    info_products = []
    products = await get_all_products_by_id(session, list(map(int, shop_cart.keys())))
    sum_product = 0
    for product in products:
        sum_product += product.price * shop_cart.get(str(product.id))
        #sum_product = [product.price * shop_cart.get(str(product.id)) for product in products]
        info_products.append(f"{shop_cart.get(str(product.id))} x {LocaleManager.get(product.name, user.lang)} "
                             f"{product.price * shop_cart.get(str(product.id))} тг\n")

    text = f'''
{LocaleManager.get('Новый заказ!', user.lang)}
{LocaleManager.get('Имя', user.lang)}: {user.name}
{LocaleManager.get('Мобильный телефон', user.lang)}: {user.phone_number}

{LocaleManager.get('Заказ', user.lang)}:
{"".join(info_products)} 

{LocaleManager.get('Итого', user.lang)}: {sum_product} ₸
'''
    return text
