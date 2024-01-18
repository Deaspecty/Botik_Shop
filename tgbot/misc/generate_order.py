from sqlalchemy.ext.asyncio import AsyncSession


from tgbot.data.locale import LocaleManager
from tgbot.models.database.product import get_all_products_by_id
from tgbot.models.database.user import User


async def show_order(
        session: AsyncSession,
        user: User,
        shop_cart: dict
):
    products = await get_all_products_by_id(session=session, shop_cart=list(map(int, shop_cart.keys())))
    sum_product = 0
    info_products = []
    for i, product in enumerate(products):
        sum_product += product.price * shop_cart.get(str(product.id))
        #sum_product = [product.price * shop_cart[1][i] for i, product in enumerate(products)]
        info_products.append(f"{shop_cart.get(str(product.id))} x {LocaleManager.get(product.name, user.lang)} "
                             f"{product.price * shop_cart.get(str(product.id))} "
                             f"{LocaleManager.get('сум', user.lang)}\n")

    text = f'''
{LocaleManager.get('Ваш заказ', user.lang)}:
{"".join(info_products)}

{LocaleManager.get('Итого', user.lang)}: {sum_product} {LocaleManager.get('сум', user.lang)}
{LocaleManager.get('Для оплаты перейдите по <a href = "https://www.google.kz/?hl=ru">ссылке</a> и оплатите', user.lang)} {sum_product} {LocaleManager.get('сум', user.lang)}
{LocaleManager.get('Чек оплаты прикрепить, нажав кнопку "Прикрепить чек" ниже (скриншот чека или pdf)', user.lang)}'''
    return text

