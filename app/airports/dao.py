from app.dao.base import BaseDAO
from app.models.airports import Airport
from app.database import async_session_maker
from sqlalchemy import select

class AirportDAO(BaseDAO):
    model = Airport

    @classmethod
    async def find_by_city(cls, city_query: str):
        async with async_session_maker() as session:
            stmt = select(cls.model).where(cls.model.city.ilike(f"%{city_query}%"))
            result = await session.execute(stmt)
            return result.scalars().all()