import pytest
from unittest.mock import AsyncMock, patch
from app.services.ticket_service import TicketService
from app.schemas.ticket_schemas import SAddTicket, SUpdateTicket
from app.exceptions.TicketExceptions import TicketNotFound, NoTicketsForUser


@pytest.mark.asyncio
class TestTicketService:

    @patch("app.services.ticket_service.TicketRepository")
    async def test_get_user_tickets_success(self, mock_repo):
        mock_repo.find_all = AsyncMock(return_value=[{"id": 1}, {"id": 2}])
        result = await TicketService.get_user_tickets(user_id=1)
        assert len(result) == 2

    @patch("app.services.ticket_service.TicketRepository")
    async def test_get_user_tickets_not_found(self, mock_repo):
        mock_repo.find_all = AsyncMock(return_value=[])
        with pytest.raises(NoTicketsForUser):
            await TicketService.get_user_tickets(user_id=1)

    @patch("app.services.ticket_service.TicketRepository")
    @patch("app.services.ticket_service.FlightRepository")
    @patch("app.services.ticket_service.PassengerRepository")
    async def test_add_ticket_success(self, mock_passenger, mock_flight, mock_ticket):
        mock_passenger.check_passenger = AsyncMock()
        mock_flight.check_flight = AsyncMock()
        mock_ticket.add = AsyncMock(return_value={"id": 1, "seat_number": "12A"})

        ticket_data = SAddTicket(passenger_id=1, flight_id=10, seat_number="12A", price=5000)
        result = await TicketService.add_ticket(ticket_data, user_id=1)
        assert result["message"] == "Билет успешно добавлен!"
        assert result["ticket"]["id"] == 1

    @patch("app.services.ticket_service.TicketRepository")
    @patch("app.services.ticket_service.FlightRepository")
    @patch("app.services.ticket_service.PassengerRepository")
    async def test_add_ticket_failure(self, mock_passenger, mock_flight, mock_ticket):
        mock_passenger.check_passenger = AsyncMock()
        mock_flight.check_flight = AsyncMock()
        mock_ticket.add = AsyncMock(return_value=None)

        ticket_data = SAddTicket(passenger_id=1, flight_id=10, seat_number="12A", price=5000)
        result = await TicketService.add_ticket(ticket_data, user_id=1)
        assert result["message"] == "Ошибка при добавлении билета!"

    @patch("app.services.ticket_service.TicketRepository")
    async def test_update_ticket_success(self, mock_repo):
        mock_repo.check_ticket = AsyncMock()
        mock_repo.update_ticket_info = AsyncMock(return_value=1)

        update_data = SUpdateTicket(seat_number="15B")
        result = await TicketService.update_ticket(ticket_id=1, update_data=update_data)
        assert result["message"] == "Билет 1 успешно обновлён!"

    @patch("app.services.ticket_service.TicketRepository")
    async def test_update_ticket_failure(self, mock_repo):
        mock_repo.check_ticket = AsyncMock()
        mock_repo.update_ticket_info = AsyncMock(return_value=0)

        update_data = SUpdateTicket(price=4500)
        result = await TicketService.update_ticket(ticket_id=99, update_data=update_data)
        assert result["message"] == "Не удалось обновить билет 99"

    @patch("app.services.ticket_service.TicketRepository")
    async def test_delete_ticket_success(self, mock_repo):
        mock_repo.delete = AsyncMock(return_value=1)
        result = await TicketService.delete_ticket(ticket_id=1)
        assert result["message"] == "Билет с id 1 удален!"

    @patch("app.services.ticket_service.TicketRepository")
    async def test_delete_ticket_not_found(self, mock_repo):
        mock_repo.delete = AsyncMock(return_value=0)
        with pytest.raises(TicketNotFound):
            await TicketService.delete_ticket(ticket_id=404)
