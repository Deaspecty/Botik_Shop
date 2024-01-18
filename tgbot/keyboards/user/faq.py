from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import LocaleManager
from tgbot.data.FAQ_info import faq_btns
from tgbot.keyboards import generate
from tgbot.keyboards.query_cb import FAQCallback


async def get_faq_btns(loc: str,
                       lang: str = "rus"):
    markup = InlineKeyboardMarkup()
    btns= {}
    for i, val in enumerate(faq_btns):
        if loc != str(i + 1):
            btns[LocaleManager.get(val, lang)] = FAQCallback.new(
                id=i + 1,
                action="faq"
            )

    return generate.GenerateMarkupButtons(
        laylout=1,
        markup=markup,
        keyboards=[
            InlineKeyboardButton(
                text=t,
                callback_data=c
            ) for t, c in btns.items()
        ]
    ).get()