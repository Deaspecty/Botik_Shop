from aiogram.types.message import Message, ContentType
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.misc.states.user import AuthUser
from tgbot.models.database.user import User
from tgbot.handlers.auth import phone_handler
from tgbot.misc.parse import parse_phone
from tgbot.keyboards.user.main import get_lang_btns
from tgbot.handlers.user.start import start_handler


async def auth_name_handler(
        message: Message,
        state: FSMContext
):
    text = "Введите ваше имя"
    await state.finish()

    msg = await message.answer(text)

    await state.update_data(msg=msg.message_id)
    await AuthUser.wait_name.set()


async def auth_lang_handler(
        message: Message,
        state: FSMContext
):
    data = await state.get_data()
    await state.update_data(name=message.text)
    await message.bot.delete_message(message.from_user.id, data['msg'])
    await message.bot.delete_message(message.from_user.id, message.message_id)
    msg = await message.answer(
        text="Выберите язык",
        reply_markup=await get_lang_btns('lang_auth')
    )

    await state.update_data(msg=msg.message_id)
    await AuthUser.wait_lang.set()


async def auth_phone_handler(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: dict
):
    data = await state.get_data()
    lang = callback_data['lang']
    await state.update_data(lang=lang)
    await callback.bot.delete_message(callback.from_user.id, callback.message.message_id)
    await phone_handler(callback.message, AuthUser.wait_phone)


async def auth_user_handler(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        user: User
):
    data = await state.get_data()
    name = data.get('name')
    lang = data.get('lang')
    phone_number = parse_phone(message.contact.phone_number)

    user.name = name
    user.phone_number = phone_number
    user.lang = lang
    await user.save(session)
    await message.answer("Вы успешно авторизовались.")
    await state.finish()
    await start_handler(message)

