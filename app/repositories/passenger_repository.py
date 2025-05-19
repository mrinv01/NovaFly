from sqlalchemy import select
from app.repositories.base_repository import BaseRepository
from app.database import async_session_maker
from app.models.passenger import Passenger
from app.exceptions.PassengerExceptions import PassengerNotFound

class PassengerRepository(BaseRepository):
    model = Passenger

    @classmethod
    async def check_passenger(cls, order_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=order_id)
            result_order = await session.execute(query)
            order = result_order.scalar_one_or_none()
            if not order:
                raise PassengerNotFound(order_id)
