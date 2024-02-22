from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message, ContentTypes, ParseMode
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.misc.delete import remove
from tgbot.misc.states.user import CoopState, UserState
from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.keyboards.query_cb import BackCallback
from tgbot.keyboards.user.coop import confirm_btns
from tgbot.keyboards.user.main import user_main_btns
from tgbot.misc.notification.notification_for_admin import send_questionnaire


async def coop_main_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext
):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text=f"⬅️{LocaleManager.get('Назад', user.lang)}",
        callback_data=BackCallback.new(
            level=0,
            action="back"
        )
    ))
    await remove(message, 1)
    await message.delete()
    text = '''Напишите ответы на вопросы ниже и отправьте одним сообщением в этот же чат:
<i>Имя представителя</i>
<i>Должность</i>
<i>Город</i>
<i>Соц.сети</i>
<i>Сайт</i>
<i>Телефон</i>
'''
    await message.answer(LocaleManager.get(text, user.lang),
                         reply_markup=markup,
                         parse_mode=ParseMode.HTML)
    await CoopState.wait_user.set()


async def get_questionnaire_handler(
        message: Message,
        session: AsyncSession,
        user: User,
        state: FSMContext,
):
    await state.update_data(quest=message.text)
    await remove(message, 1)
    await message.delete()
    text = (LocaleManager.get("Подтвердите пожалуйста!", user.lang) + "\n"
            + LocaleManager.get("Вы написали:", user.lang) + "\n"
            + message.text)
    await message.answer(text,
                         reply_markup=await confirm_btns(user.lang))


async def confirm_handler(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User,
        callback_data: dict,
        state: FSMContext
):
    data = await state.get_data()
    answer = callback_data['answer']
    if answer == "no":
        return await coop_main_handler(
            message=callback.message,
            session=session,
            state=state,
            user=user
        )

    await send_questionnaire(
        session=session,
        bot=callback.bot,
        text=data.get('quest')
    )
    await callback.message.delete()
    await callback.message.answer(
        text=LocaleManager.get("Спасибо за обращение, мы скоро с вами свяжемся", user.lang) + " 🤗",
        reply_markup=user_main_btns(user.lang)
    )
    await UserState.wait_user.set()
