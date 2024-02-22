import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message

from tgbot.models.database.user import User
from tgbot.data.locale import LocaleManager


class TextKeyboardFilter(BoundFilter):


    def __init__(self, text: typing.List[str], is_not=False):
        self.text = text
        self.is_not = is_not

    async def check(self, m: Message) -> bool:
        locale_manager = LocaleManager
        m_answer = m.text
        if "🇰🇿🇷🇺🇺🇿" in m_answer:
            m_answer = m_answer.replace(" 🇰🇿🇷🇺🇺🇿", "")
        data = ctx_data.get()
        user: User = data.get('user')

        if isinstance(self.text, str):
            self.text = [self.text]

        locale_data = locale_manager.data.get(user.lang)
        for text in self.text:
            if "🇰🇿🇷🇺🇺🇿" in text:
                text = text.replace(" 🇰🇿🇷🇺🇺🇿", "")
            for key, value in locale_data.items():
                if not value:
                    key = value
                if key == text and value == m_answer:
                    return True

                if key == text and key == m_answer:
                    return True
