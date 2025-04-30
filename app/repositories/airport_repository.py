from app.repositories.base_repository import BaseRepository
from app.models.airports import Airport
from app.database import async_session_maker
from sqlalchemy import select
from app.exceptions.AirportExceptions import AirportExceptions

class AirportRepository(BaseRepository):
    model = Airport

    @classmethod
    async def find_by_city(cls, city_query: str):
        async with async_session_maker() as session:
            stmt = select(cls.model).where(cls.model.city.ilike(f"%{city_query}%"))
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def check_airport(cls, airport_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=airport_id)
            result_order = await session.execute(query)
            order = result_order.scalar_one_or_none()
            if not order:
                raise AirportExceptions.AirportNotFound(airport_id)