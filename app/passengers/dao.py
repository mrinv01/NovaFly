from sqlalchemy import select
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.models.passenger import Passenger
from app.exceptions.PassengerExceptions import PassengerExceptions

class PassengerDAO(BaseDAO):
    model = Passenger

    @classmethod
    async def check_passenger(cls, order_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=order_id)
            result_order = await session.execute(query)
            order = result_order.scalar_one_or_none()
            if not order:
                raise PassengerExceptions.PassengerNotFound(order_id)
