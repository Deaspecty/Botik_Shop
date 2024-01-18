from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import LocaleManager
from tgbot.data.FAQ_info import faq_btns
from tgbot.keyboards import generate
from tgbot.keyboards.query_cb import ConfirmCallback


async def confirm_btns(lang: str = "rus"):
    markup = InlineKeyboardMarkup()
    btns={
        LocaleManager.get('Да', lang): ConfirmCallback.new(
            answer="yes",
            action="coop"
        ), LocaleManager.get('Изменить текст', lang): ConfirmCallback.new(
            answer="no",
            action="coop"
        )
    }

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
