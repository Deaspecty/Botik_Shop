import asyncio
from typing import Sequence

from sqlalchemy import (BigInteger, Column, String, select,
                        Date, DateTime, func, Integer, ForeignKey, Boolean)
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import Lang
from tgbot.models.database.base import Base
from sqlalchemy.orm import relationship


#class ProductPhoto(Base):
#    __tablename__ = 'products_photo'
#    id = Column(
#        Integer,
#        primary_key=True,
#        autoincrement=True
#    )
#    product_id = Column(
#        Integer,
#        ForeignKey('products.id', ondelete='CASCADE')
#    )

#    path = Column(String)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(
        String(200)
    )
    description = Column(
        String(1000)
    )
    price = Column(
        BigInteger
    )
    photo_path = Column(String(200))
    #photos = relationship(ProductPhoto)


async def get_all_products(session: AsyncSession) -> Sequence[Product]:
    stmt = select(Product)
    response = await session.execute(stmt)
    return response.scalars().all()


async def get_all_products_by_id(session: AsyncSession,
                                 shop_cart: list) -> Sequence[Product]:
    stmt = select(Product).filter(Product.id.in_(shop_cart))
    response = await session.execute(stmt)
    return response.scalars().all()


async def get_product_by_id(session: AsyncSession,
                            product_id: int) -> Product:
    stmt = select(Product).where(Product.id == product_id)
    response = await asyncio.ensure_future(session.execute(stmt))
    return response.scalars().one()

