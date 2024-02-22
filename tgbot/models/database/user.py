from typing import Sequence
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
    lang = Column(String(16))
    region = Column(String(50))
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

    @classmethod
    async def get_by_region(
            cls,
            session: AsyncSession,
            region: str
    ) -> Sequence['User']:
        stmt = select(User).where(
            User.id == region
        )

        return await session.scalar(stmt)

    @classmethod
    async def get_all_admins(
            cls,
            session: AsyncSession) -> Sequence['User']:
        stmt = select(User).where(
            User.is_admin == True
        )
        response = await session.execute(stmt)
        return response.scalars().all()

    def get_mention(self, name=None):
        if name is None:
            name = self.name

        return f"<a href='{self.id}'>{self.name}</a>"


class Admin(Base):
    __tablename__ = "admins"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tlg_id = Column(BigInteger)
    phone_number = Column(String(16), unique=True)
    region = Column(String(50))

    @classmethod
    async def get_admins(
            cls,
            session: AsyncSession) -> Sequence['Admin']:
        stmt = select(Admin)
        response = await session.execute(stmt)
        return response.scalars().all()
