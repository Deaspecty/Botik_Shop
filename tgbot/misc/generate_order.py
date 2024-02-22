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
    currency = "тг"
    link_pay = "https://pay.kaspi.kz/pay/zzkyicl2"
    price = 0.037
    if user.region == 'Russia':
        currency = '₽'
        link_pay = "https://www.google.kz/?hl=ru"
        price = 0.0074
    if user.region == 'Uzbekistan':
        currency = 'сум'
        link_pay = "https://www.google.kz/?hl=ru"
        price = 1
    for i, product in enumerate(products):
        sum_product += product.price * shop_cart.get(str(product.id))
        #sum_product = [product.price * shop_cart[1][i] for i, product in enumerate(products)]
        info_products.append(f"{shop_cart.get(str(product.id))} x {LocaleManager.get(product.name, user.lang)} "
                             f"{int(product.price * shop_cart.get(str(product.id)) * price)} "
                             f"{LocaleManager.get(currency, user.lang)}\n")

    info = f'''
- в городах Алматы, Астана, Шымкент, Караганда со склада Ederra осуществляется Яндекс курьером за счет покупателя согласно тарифу на момент отправки заказа;
- в другие города Казахстана осуществляется ТК CDEK со склада в городе Алматы за счет покупателя согласно тарифу на момент отправки заказа.'''
    if user.region == "Russia":
        info = f'''
- в городе Москва со склада Ederra осуществляется Яндекс курьером за счет покупателя согласно тарифу на момент отправки заказа;
- в другие города России осуществляется ТК CDEK со склада в городе Москва за счет покупателя согласно тарифу на момент отправки заказа.'''
    elif user.region == 'Uzbekistan':
        info = f'''
- в городе Ташкент со склада Ederra осуществляется Яндекс курьером за счет покупателя согласно тарифу на момент отправки заказа;
- в другие города Узбекистана осуществляется ТК CDEK со склада в городе Ташкент за счет покупателя согласно тарифу на момент отправки заказа.'''

    text = f'''
{LocaleManager.get('Ваш заказ', user.lang)}:
{"".join(info_products)}
{LocaleManager.get('<b>Итого</b>', user.lang)}: {int(sum_product * price)} {LocaleManager.get(currency, user.lang)}

{LocaleManager.get(f'Для оплаты перейдите по <a href = "{link_pay}">ссылке</a> и оплатите', user.lang)} {int(sum_product * price)} {LocaleManager.get(currency, user.lang)} {LocaleManager.get("paymentsEddera", user.lang)}
{LocaleManager.get('Чек оплаты прикрепить, нажав кнопку "Прикрепить чек" ниже (скриншот чека или pdf)', user.lang)}
{LocaleManager.get('Важно! Укажите информацию для доставки после прикрепления чека оплаты.', user.lang)}

{LocaleManager.get('Доставка', user.lang)}:
{LocaleManager.get(info, user.lang)}

{LocaleManager.get('После прикрепления чека оплаты, указать одним сообщением', user.lang)}:
1. {LocaleManager.get('Имя получателя', user.lang)};
2. {LocaleManager.get('Полный адрес, который отображается на Яндекс карте', user.lang)};
3. {LocaleManager.get('Телефон для связи', user.lang)};
'''
    return text.replace("paymentsEddera", "")
