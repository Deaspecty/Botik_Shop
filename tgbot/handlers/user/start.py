from aiogram.types.message import Message

from tgbot.data.locale import LocaleManager
from tgbot.models.database.user import User
from tgbot.keyboards.user.main import user_main_btns
from tgbot.misc.states.user import UserState
from tgbot.misc.delete import remove
from aiogram.dispatcher.storage import FSMContext


async def start_handler(
        message: Message,
        user: User,
        state: FSMContext
):
    data = await state.get_data()
    if data.get('msg_id_text'):
        try:
            await message.bot.delete_message(message.chat.id, data.get('msg_id_text'))
        except:
            pass
    await remove(message, 1)
    text = '''Добро пожаловать в магазин нашей компании
Для выбора продукции перейдите в Каталог в главном меню ниже
'''
    await message.answer(
        text=LocaleManager.get(text, user.lang) + " ⬇️",
        reply_markup=user_main_btns(user.lang)
    )
    await UserState.wait_user.set()
