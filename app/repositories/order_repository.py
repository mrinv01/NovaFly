from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update as sqlalchemy_update, select
from app.models.order import Order
from app.repositories.base_repository import BaseRepository
from app.database import async_session_maker
from app.exceptions.OrderExceptions import OrderNotFound

class OrderRepository(BaseRepository):
    model = Order

    @classmethod
    async def check_order(cls, order_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=order_id)
            result_order = await session.execute(query)
            order = result_order.scalar_one_or_none()
            if not order:
                raise OrderNotFound(order_id)

    @classmethod
    async def update_status(cls, order_id: int, new_status: str) -> int:
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(cls.model.id == order_id)
                    .values(status=new_status)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

