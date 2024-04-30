from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.keyboards.user.main import get_product_btns


async def show_product_function(
        callback: CallbackQuery,
        session: AsyncSession,
        state: FSMContext,
        callback_data: dict,
        user: User,
        action: str
):
    data = await state.get_data()
    count = 0
    product_id = callback_data.get('product_id')
    if data.get('shop_cart') is not None:
        if data.get('shop_cart').get(product_id):
            count = int(data.get('shop_cart').get(product_id))
    else:
        data['shop_cart'] = {}

    if callback_data.get('turn') is not None:
        count = count + int(callback_data.get('turn'))

    if count < 0:
        count = 0

    data['shop_cart'][product_id] = count
    if count == 0 and data.get('shop_cart').get(product_id) is not None:
        data['shop_cart'].pop(product_id)

    btns, product = await get_product_btns(
        session=session,
        product_id=product_id,
        action=action,
        count=count,
        lang=user.lang,
        shop_cart=data.get('shop_cart')
    )
    price = product.price

    text = f'''
{LocaleManager.get('Название', user.lang)}: {LocaleManager.get(product.name, user.lang)}

{LocaleManager.get('Описание', user.lang)}: {LocaleManager.get(product.description, user.lang)}

{LocaleManager.get('Цена', user.lang)}: {int(price)}
    '''
    if callback_data.get('turn') is None:
        await callback.message.delete()
        await callback.message.answer_photo(photo=open(product.photo_path, "rb"), caption=text, reply_markup=btns)
    else:
        try:
            await callback.message.edit_reply_markup(reply_markup=btns)
        except:
            pass
    await state.update_data(shop_cart=data['shop_cart'])
