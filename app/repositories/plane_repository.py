from app.repositories.base_repository import BaseRepository
from app.models.plane import Plane
from sqlalchemy import update as sqlalchemy_update, select, delete as sqlalchemy_delete
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.PlaneExceptions import PlaneNotFound


class PlaneRepository(BaseRepository):
    model = Plane

    @classmethod
    async def check_plane(cls, plane_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=plane_id)
            result_order = await session.execute(query)
            order = result_order.scalar_one_or_none()
            if not order:
                raise PlaneNotFound(plane_id)

    @classmethod
    async def update_plane_info(cls, plane_id: int, **update_fields) -> int:
        if not update_fields:
            return 0  # Нечего обновлять

        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(cls.model.id == plane_id)
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

    @classmethod
    async def delete_by_ids(cls, ids: list[int]) -> int:
        if not ids:
            raise ValueError("Список ID не может быть пустым.")

        async with async_session_maker() as session:
            async with session.begin():
                stmt = sqlalchemy_delete(cls.model).where(cls.model.id.in_(ids))
                result = await session.execute(stmt)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount