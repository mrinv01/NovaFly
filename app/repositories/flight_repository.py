from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import update as sqlalchemy_update, select
from app.models.flight import Flight
from app.repositories.base_repository import BaseRepository
from app.database import async_session_maker
from app.exceptions.FlightExceptions import FlightNotFound


class FlightRepository(BaseRepository):
    model = Flight

    @classmethod
    async def check_flight(cls, flight_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=flight_id)
            result_order = await session.execute(query)
            order = result_order.scalar_one_or_none()
            if not order:
                raise FlightNotFound(flight_id)

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
