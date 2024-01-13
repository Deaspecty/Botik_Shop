from sqlalchemy import BigInteger, Column, String, select, Date, DateTime, func, Integer, ForeignKey, Boolean
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import Lang
from tgbot.models.database.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200))
    fullname = Column(String(200))
    phone_number = Column(String(16), unique=True)
    created_at = Column(DateTime, server_default=func.now())
    lang = Column(String(16), default=Lang.RUS)
    is_admin = Column(Boolean, default=False)

    @classmethod
    async def get_by_id(
            cls,
            session: AsyncSession,
            user_id: int
    ) -> 'User':
        stmt = select(User).where(
            User.id == user_id
        )

        return await session.scalar(stmt)

    def get_mention(self, name=None):
        if name is None:
            name = self.name

        return f"<a href='{self.id}'>{self.name}</a>"

