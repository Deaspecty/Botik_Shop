from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message, ContentTypes, ParseMode
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.models.database.order import Order, OrderItem
from tgbot.handlers.user.start import start_handler
from tgbot.handlers.auth import phone_handler
from tgbot.keyboards.query_cb import ReceiptCallback, BackCallback
from tgbot.keyboards.user.main import user_main_btns, get_shop_cart_btns, get_back_btns
from tgbot.misc.notification.notification_for_admin import generate_admin_notification
from tgbot.misc.generate_order import show_order
from tgbot.misc.show_product import show_product_function
from tgbot.misc.states.user import ShopCart, UserState
from tgbot.misc.delete import remove
from tgbot.misc.parse import parse_phone


async def shop_cart_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    data = await state.get_data()
    products = []
    counts = []
    loc = data.get('loc_cart')
    if data.get('shop_cart') is not None:
        for i in data.get('shop_cart').items():
            if i[1]:
                products.append(int(i[0]))
                counts.append(i[1])

    btns = await get_shop_cart_btns(
        session=session,
        shop_cart=products,
        counts=counts,
        lang=user.lang,
        loc=int(loc) if loc is not None else 0
    )
    await remove(message, 1)
    await message.delete()
    if products:
        await message.answer(
            text=LocaleManager.get("Ваша корзина", user.lang),
            reply_markup=btns
        )
        await ShopCart.wait_product.set()
    else:
        await message.answer(
            text=LocaleManager.get("В корзине пусто", user.lang),
            reply_markup=user_main_btns(lang=user.lang)
        )


async def shop_cart_quantity_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        callback_data: dict,
        user: User,
        state: FSMContext
):
    await show_product_function(callback, session, state, callback_data, user, 'cart')


async def clear_shop_cart_handler(
        callback: CallbackQuery,
        user: User,
        state: FSMContext
):
    await callback.message.delete()
    await state.finish()
    await start_handler(
        message=callback.message,
        user=user
    )


async def remove_product_cart_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User,
        callback_data: dict,
        state: FSMContext
):
    product_id = callback_data.get('shop_cart')
    data = await state.get_data()
    data['shop_cart'].pop(product_id)
    await state.update_data(shop_cart=data['shop_cart'])
    loc = data.get('loc_cart')
    if loc is not None:
        loc = 0 if loc > len(data['shop_cart'].keys()) - 1 else loc
    await state.update_data(loc_cart=loc)
    await shop_cart_handler(message=callback.message,
                            session=session,
                            state=state,
                            user=user)


async def purchase_shop_cart_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User,
        callback_data: dict,
        state: FSMContext
):
    data = await state.get_data()
    #shop_cart = callback_data.get('shop_cart')
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text=LocaleManager.get("Прикрепить чек", user.lang),
        callback_data=ReceiptCallback.new(
            receipt='check',
            action='receipt'
        )
    ))
    markup.add(InlineKeyboardButton(
        text=f"⬅️{LocaleManager.get('Назад', user.lang)}",
        callback_data=BackCallback.new(
            level="1_cart",
            action="back"
        )
    ))
    markup.add(InlineKeyboardButton(
        text=f"⬅️{LocaleManager.get('Назад на главную', user.lang)}",
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    ))

    await callback.message.edit_text(
        text=await show_order(session=session, shop_cart=data.get('shop_cart'), user=user),
        reply_markup=markup,
        parse_mode=ParseMode.HTML
    )


async def send_receipt_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    await callback.message.delete()
    if user.phone_number:
        markup = await get_back_btns(user.lang)
        msg = await callback.message.answer(
            text=LocaleManager.get("Скиньте скриншот чека или pdf", user.lang),
            reply_markup=markup
        )
        await state.update_data(msg=msg.message_id)
        await ShopCart.wait_file.set()
    else:
        await phone_handler(m=callback.message,
                            user=user,
                            state=ShopCart.wait_phone)


async def save_phone_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    data = await state.get_data()

    phone_number = parse_phone(message.contact.phone_number)
    user.phone_number = phone_number
    await user.save(session)

    markup = await get_back_btns(user.lang)
    await remove(message, 1)
    await remove(message, 2)
    #await message.bot.delete_message(message.from_user.id, data['msg'])
    msg = await message.answer(
        text=LocaleManager.get("Скиньте скриншот чека или pdf", user.lang),
        reply_markup=markup
    )
    await state.update_data(msg=msg.message_id)
    await ShopCart.wait_file.set()


async def get_picture_or_pdf_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    data = await state.get_data()
    shop_cart = data['shop_cart']
    await message.delete()
    await message.bot.delete_message(message.from_user.id, data['msg'])
    admins = await User.get_all_admins(session)
    markup = await get_back_btns(user.lang)
    if (message.content_type not in ContentTypes.PHOTO and
            message.content_type not in ContentTypes.DOCUMENT):

        msg = await message.answer(
            text=LocaleManager.get("Вы отправили не правильный файл, пожалуйста "
                                   "Скиньте скриншот чека или файл в формате pdf", user.lang),
            reply_markup=markup
        )
        await state.update_data(msg=msg.message_id)
        return

    if message.document:
        if message.document.file_name[-4::1] != '.pdf':
            msg = await message.answer(
                text=LocaleManager.get("Ваш файл не в формате pdf. "
                                       "Cкиньте скриншот чека или файл в формате pdf", user.lang),
                reply_markup=markup
            )
            await state.update_data(msg=msg.message_id)
            return
        file_id = message.document.file_id
        for admin in admins:
            text = await generate_admin_notification(
                session=session,
                shop_cart=shop_cart,
                user=user,
            )
            await message.bot.send_document(chat_id=admin.id, document=file_id, caption=text)
    else:
        file_id = message.photo[-1].file_id
        for admin in admins:
            text = await generate_admin_notification(
                session=session,
                shop_cart=shop_cart,
                user=user,
            )
            await message.bot.send_photo(chat_id=admin.id, photo=file_id, caption=text)

    order = Order(
        user_id=user.id
    )
    session.add(order)
    await session.commit()
    for key, val in shop_cart.items():
        order_item = OrderItem(
            order_id=order.id,
            product_id=int(key),
            quantity=val
        )
        session.add(order_item)
    await session.commit()
    await state.finish()
    await message.answer(
        text=LocaleManager.get("Спасибо за покупку, скоро администратор примет вашу заявку", user.lang),
        reply_markup=user_main_btns(user.lang))
    await UserState.wait_user.set()
