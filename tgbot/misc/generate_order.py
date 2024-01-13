from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.models.database.product import get_all_products_by_id


async def show_order(
        session: AsyncSession,
        shop_cart: list
):
    products = await get_all_products_by_id(session=session, shop_cart=shop_cart[0])
    sum_product = [product.price * shop_cart[1][i] for i, product in enumerate(products)]
    info_products = [f"{shop_cart[1][i]} x {product.name} {product.price * shop_cart[1][i]} тг\n" for i, product in enumerate(products)]

    text = f'''
Ваш заказ:
{"".join(info_products)}

Итого: {sum(sum_product)} ₸
Для оплаты перейдите по ссылке и оплатите {sum(sum_product)} ₸
Чек оплаты прикрепить, нажав кнопку "Прикрепить чек" ниже (скриншот чека или pdf)
Ссылка: https://www.google.kz/?hl=ru'''
    return text

