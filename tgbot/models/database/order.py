from sqlalchemy import (BigInteger, Column, String, select, Date, DateTime,
                        func, Integer, ForeignKey, Boolean, )
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.data.locale import Lang
from tgbot.models.database.base import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        BigInteger,
        ForeignKey('users.id', ondelete='CASCADE')
    )
    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    products_orders = relationship(
        'OrderItem',
        primaryjoin='OrderItem.order_id == Order.id',
        uselist=True
    )


class OrderItem(Base):
    __tablename__ = 'orders_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))

    quantity = Column(Integer, default=0)

    product = relationship(
        'Product', foreign_keys=[product_id], uselist=False
    )