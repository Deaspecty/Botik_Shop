from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import Poll, PollAnswer, CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from tgbot.models.database.user import User


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        pool = obj.bot.get('pool')
        session: AsyncSession = pool()

        if not isinstance(obj, (Message, CallbackQuery)):
            data['session'] = session
            return

        if not (user := await session.get(User, obj.from_user.id)):
            user = User(
                id=obj.from_user.id,
                fullname=obj.from_user.full_name
            )
            session.add(user)
            await session.commit()

        data['session'] = session
        data['user'] = user

    async def post_process(self, obj, data, *args):
        if session := data.get("session"):
            await session.close()
            data.pop('session')
