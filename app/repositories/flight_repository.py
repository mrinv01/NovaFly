from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update as sqlalchemy_update
from app.models.flight import Flight
from app.repositories.base_repository import BaseDAO
from app.database import async_session_maker


class FlightDAO(BaseDAO):
    model = Flight

    @classmethod
    async def update_flight_info(cls, flight_id: int, **update_fields) -> int:
        if not update_fields:
            return 0  # Нечего обновлять

        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(cls.model.id == flight_id)
                    .values(**update_fields)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

                return result.rowcount
