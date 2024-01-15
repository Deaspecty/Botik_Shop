from tracemalloc import BaseFilter

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from tgbot.models.database.user import User


class AuthFilter(BoundFilter):
    key = 'is_auth'

    def __init__(self, is_auth):
        self.is_auth = is_auth

    async def check(self, *args) -> bool:
        data = ctx_data.get()
        user: User = data.get('user')

        if not user.name and not self.is_auth:
            return True

        if user.name and self.is_auth:
            return True

