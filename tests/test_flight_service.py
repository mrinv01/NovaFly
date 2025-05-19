import pytest
from unittest.mock import AsyncMock, patch
from datetime import date, time

from app.services.flight_service import FlightService
from app.schemas.flight_schemas import SAddFlight, SUpdateFlight
from app.schemas.request_body_flight import RequestBodyFlight
from app.exceptions.FlightExceptions import InformationNotFoundException, NoFlights, FlightNotFound

@pytest.mark.asyncio
@patch("app.services.flight_service.AirportRepository")
@patch("app.services.flight_service.PlaneRepository")
@patch("app.services.flight_service.FlightRepository")
class TestFlightService:

    async def test_get_all_flights_success(self, mock_flight_repo, _, __):
        mock_flight_repo.find_all = AsyncMock(return_value=[{"id": 1}])
        result = await FlightService.get_all_flights()
        assert result == [{"id": 1}]
        mock_flight_repo.find_all.assert_awaited_once()

    async def test_get_all_flights_empty(self, mock_flight_repo, _, __):
        mock_flight_repo.find_all = AsyncMock(return_value=[])
        with pytest.raises(NoFlights):
            await FlightService.get_all_flights()

    async def test_get_flight_by_filter_success(self, mock_flight_repo, _, __):
        body = RequestBodyFlight(status="Готов")
        mock_flight_repo.find_all = AsyncMock(return_value=[{"id": 2}])
        result = await FlightService.get_flight_by_filter(body)
        assert result[0]["id"] == 2
        mock_flight_repo.find_all.assert_awaited_once_with(status="Готов")

    async def test_get_flight_by_filter_not_found(self, mock_flight_repo, _, __):
        body = RequestBodyFlight(status="Отменен")
        mock_flight_repo.find_all = AsyncMock(return_value=[])
        with pytest.raises(InformationNotFoundException):
            await FlightService.get_flight_by_filter(body)

    async def test_get_flight_by_id_found(self, mock_flight_repo, _, __):
        mock_flight_repo.find_one_or_none_by_id = AsyncMock(return_value={"id": 3})
        result = await FlightService.get_flight_by_id(3)
        assert result["id"] == 3
        mock_flight_repo.find_one_or_none_by_id.assert_awaited_once_with(3)

    async def test_get_flight_by_id_not_found(self, mock_flight_repo, _, __):
        mock_flight_repo.find_one_or_none_by_id = AsyncMock(return_value=None)
        with pytest.raises(InformationNotFoundException):
            await FlightService.get_flight_by_id(404)

    async def test_add_flight_success(self, mock_flight_repo, mock_plane_repo, mock_airport_repo):
        new_flight = SAddFlight(
            plane_id=1,
            departure_from=10,
            arrival_to=20,
            departure_date=date(2025, 1, 1),
            departure_time=time(12, 0),
            arrival_date=date(2025, 1, 1),
            arrival_time=time(14, 0),
            status="Готов"
        )

        mock_plane_repo.check_plane = AsyncMock()
        mock_airport_repo.check_airport = AsyncMock()
        mock_flight_repo.add = AsyncMock(return_value=True)

        result = await FlightService.add_flight(new_flight)

        mock_plane_repo.check_plane.assert_awaited_once_with(1)
        mock_airport_repo.check_airport.assert_any_await(10)
        mock_airport_repo.check_airport.assert_any_await(20)
        mock_flight_repo.add.assert_awaited_once_with(**new_flight.model_dump())

        assert result["message"] == "Рейс успешно создан!"
        assert result["flight"] == new_flight

    async def test_add_flight_failure(self, mock_flight_repo, mock_plane_repo, mock_airport_repo):
        new_flight = SAddFlight(
            plane_id=1,
            departure_from=10,
            arrival_to=20,
            departure_date=date(2025, 1, 1),
            departure_time=time(12, 0),
            arrival_date=date(2025, 1, 1),
            arrival_time=time(14, 0),
            status="Готов"
        )

        mock_plane_repo.check_plane = AsyncMock()
        mock_airport_repo.check_airport = AsyncMock()
        mock_flight_repo.add = AsyncMock(return_value=False)

        result = await FlightService.add_flight(new_flight)

        assert result["message"] == "При создании рейса произошла ошибка!"

    async def test_update_flight_success(self, mock_flight_repo, _, __):
        update = SUpdateFlight(
            plane_id=2,
            departure_from=11,
            arrival_to=21,
            departure_date=date(2025, 2, 1),
            departure_time=time(15, 0),
            arrival_date=date(2025, 2, 1),
            arrival_time=time(17, 0),
            status="Отменен"
        )
        mock_flight_repo.update_flight_info = AsyncMock(return_value=1)

        result = await FlightService.update_flight(5, update)

        mock_flight_repo.update_flight_info.assert_awaited_once()
        assert result["message"] == "Рейс 5 успешно обновлён"

    async def test_update_flight_not_found(self, mock_flight_repo, _, __):
        update = SUpdateFlight(
            plane_id=2,
            departure_from=11,
            arrival_to=21,
            departure_date=date(2025, 2, 1),
            departure_time=time(15, 0),
            arrival_date=date(2025, 2, 1),
            arrival_time=time(17, 0),
            status="Отменен"
        )
        mock_flight_repo.update_flight_info = AsyncMock(return_value=0)

        with pytest.raises(InformationNotFoundException):
            await FlightService.update_flight(999, update)
