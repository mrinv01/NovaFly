from app.schemas.ticket_schemas import SAddTicket, SUpdateTicket
from app.repositories.ticket_repository import TicketRepository
from app.repositories.passenger_repository import PassengerRepository
from app.repositories.flight_repository import FlightRepository
from app.exceptions.TicketExceptions import TicketExceptions


class TicketService:

    @staticmethod
    async def get_user_tickets(user_id: int):
        tickets = await TicketRepository.find_all(user_id=user_id)
        if not tickets:
            raise TicketExceptions.NoTicketsForUser
        return tickets

    @staticmethod
    async def add_ticket(ticket_data: SAddTicket, user_id: int):
        await PassengerRepository.check_passenger(ticket_data.passenger_id)
        await FlightRepository.check_flight(ticket_data.flight_id)

        ticket_dict = ticket_data.model_dump()
        ticket_dict["user_id"] = user_id
        new_ticket = await TicketRepository.add(**ticket_dict)

        if new_ticket:
            return {"message": "Билет успешно добавлен!", "ticket": new_ticket}
        return {"message": "Ошибка при добавлении билета!"}

    @staticmethod
    async def update_ticket(ticket_id: int, update_data: SUpdateTicket):
        await TicketRepository.check_ticket(ticket_id)
        update_dict = update_data.model_dump(exclude_none=True)
        updated_rows = await TicketRepository.update_ticket_info(ticket_id, **update_dict)

        if updated_rows == 0:
            return {"message": f"Не удалось обновить билет {ticket_id}"}
        return {"message": f"Билет {ticket_id} успешно обновлён!"}

    @staticmethod
    async def delete_ticket(ticket_id: int):
        check = await TicketRepository.delete(id=ticket_id)
        if check:
            return {"message": f"Билет с id {ticket_id} удален!"}
        raise TicketExceptions.TicketNotFound(ticket_id)
