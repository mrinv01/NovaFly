from app.dao.base import BaseDAO
from app.models.tickets import Ticket
from sqlalchemy import update as sqlalchemy_update, select
from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from app.exceptions.TicketExceptions import TicketExceptions

class TicketDAO(BaseDAO):
    model = Ticket

    @classmethod
    async def check_ticket(cls, ticket_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=ticket_id)
            result_order = await session.execute(query)
            order = result_order.scalar_one_or_none()
            if not order:
                raise TicketExceptions.TicketNotFound(ticket_id)

    @classmethod
    async def update_ticket_info(cls, ticket_id: int, **update_fields) -> int:
        if not update_fields:
            return 0  # Нечего обновлять

        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(cls.model.id == ticket_id)
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
