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
        admin: User
):
    if not admin.lang:
        admin.lang = "rus"
    info_products = []
    products = await get_all_products_by_id(session, list(map(int, shop_cart.keys())))
    sum_product = 0
    region = "Казахстан"
    currency = 'тг'
    price = 0.037
    if user.region == 'Russia':
        region = "Россия"
        currency = '₽'
        price = 0.0074
    if user.region == 'Uzbekistan':
        region = "Узбекистан"
        currency = 'сум'
        price = 1
    for product in products:
        sum_product += product.price * shop_cart.get(str(product.id))
        #sum_product = [product.price * shop_cart.get(str(product.id)) for product in products]
        info_products.append(f"{shop_cart.get(str(product.id))} x {LocaleManager.get(product.name, admin.lang)} "
                             f"{int(product.price * shop_cart.get(str(product.id)) * price)} "
                             f"{LocaleManager.get(currency, admin.lang)}\n")
    text = f'''
{LocaleManager.get('Новый заказ!', admin.lang)}
{LocaleManager.get('Имя', admin.lang)}: {user.name}
{LocaleManager.get('Мобильный телефон', admin.lang)}: +{user.phone_number}
{LocaleManager.get('Страна', admin.lang)}: {region}
{LocaleManager.get('Заказ', admin.lang)}:
{"".join(info_products)}
{LocaleManager.get('Итого', admin.lang)}: {int(sum_product*price)} {LocaleManager.get(currency, admin.lang)}
'''
    return text


async def send_questionnaire(
        session: AsyncSession,
        bot: Bot,
        text: str
):
    admins = await User.get_all_admins(session)
    for admin in admins:
        await bot.send_message(
            admin.id,
            LocaleManager.get("Пришло новое обращение по сотрудничеству!", admin.lang) + "\n" + text)
