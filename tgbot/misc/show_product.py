from aiogram.types.message import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.user.main import user_main_btns, get_product_btns, get_shop_cart_btns
from tgbot.misc.states.user import ShopCart


async def show_product_function(
        callback: CallbackQuery,
        session: AsyncSession,
        state: FSMContext,
        callback_data: dict,
        action: str
):
    data = await state.get_data()
    count = 0
    if data.get('shop_cart').get(callback_data.get('product_id')):
        count = int(data.get('shop_cart').get(callback_data.get('product_id')))

    if callback_data.get('turn') is not None:
        count = count + int(callback_data.get('turn'))

    if count < 0:
        count = 0
    product_id = callback_data.get('product_id')
    btns, product = await get_product_btns(
        session=session,
        product_id=product_id,
        action=action,
        count=count
    )
    text = f'''
Название: {product.name}

Описание: {product.description}

Цена: {product.price}
    '''
    if callback_data.get('turn') is None:
        await callback.message.delete()
        await callback.message.answer_photo(photo=open(product.photo_path, "rb"), caption=text, reply_markup=btns)
    else:
        await callback.message.edit_reply_markup(reply_markup=btns)

    await state.update_data(shop_cart={product_id: count})
