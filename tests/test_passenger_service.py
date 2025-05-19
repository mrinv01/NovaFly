import pytest
from unittest.mock import AsyncMock, patch
from datetime import date

from app.services.passenger_service import PassengerService
from app.schemas.passenger_schemas import SCreatePassenger, SUpdatePassenger
from app.schemas.request_body_passenger import RBPassenger
from app.exceptions.PassengerExceptions import PassengerNotFound, InformationNotFound


@pytest.mark.asyncio
@patch("app.services.passenger_service.PassengerRepository")
class TestPassengerService:

    async def test_create_passenger(self, mock_repo):
        passenger_data = SCreatePassenger(
            surname="Иванов",
            name="Иван",
            patronymic="Иванович",
            date_of_birth=date(1990, 1, 1),
            document_number=1234567890
        )

        mock_repo.add = AsyncMock(return_value={"id": 1, **passenger_data.model_dump()})

        result = await PassengerService.create_passenger(passenger_data)

        mock_repo.add.assert_awaited_once()
        assert result["id"] == 1

    async def test_get_all_passengers(self, mock_repo):
        mock_repo.find_all = AsyncMock(return_value=[{"id": 1}])

        result = await PassengerService.get_all_passengers()

        assert result == [{"id": 1}]
        mock_repo.find_all.assert_awaited_once()

    async def test_get_passengers_by_filter_found(self, mock_repo):
        mock_repo.find_all = AsyncMock(return_value=[{"id": 1}])
        request_body = RBPassenger(surname="Иванов")

        result = await PassengerService.get_passengers_by_filter(request_body)

        assert result == [{"id": 1}]
        mock_repo.find_all.assert_awaited_once_with(surname="Иванов")

    async def test_get_passengers_by_filter_not_found(self, mock_repo):
        mock_repo.find_all = AsyncMock(return_value=[])
        request_body = RBPassenger(name="Неизвестный")

        with pytest.raises(InformationNotFound):
            await PassengerService.get_passengers_by_filter(request_body)

    async def test_get_passenger_by_id_found(self, mock_repo):
        mock_repo.find_one_or_none_by_id = AsyncMock(return_value={"id": 5})

        result = await PassengerService.get_passenger_by_id(5)

        assert result["id"] == 5
        mock_repo.find_one_or_none_by_id.assert_awaited_once_with(5)

    async def test_get_passenger_by_id_not_found(self, mock_repo):
        mock_repo.find_one_or_none_by_id = AsyncMock(return_value=None)

        with pytest.raises(InformationNotFound):
            await PassengerService.get_passenger_by_id(404)

    async def test_update_passenger_success(self, mock_repo):
        mock_repo.update = AsyncMock(return_value=1)

        update_data = SUpdatePassenger(name="Петр")
        result = await PassengerService.update_passenger(10, update_data)

        assert result["message"] == "Данные пассажира 10 успешно обновлены."
        mock_repo.update.assert_awaited_once()

    async def test_update_passenger_not_updated(self, mock_repo):
        mock_repo.update = AsyncMock(return_value=0)

        update_data = SUpdatePassenger(name="Николай")
        result = await PassengerService.update_passenger(999, update_data)

        assert result["message"] == "Пассажир с id 999 не найден или не обновился."

    async def test_delete_passenger_success(self, mock_repo):
        mock_repo.delete = AsyncMock(return_value=1)

        result = await PassengerService.delete_passenger(12)

        assert result["message"] == "Пассажир 12 успешно удален."
        mock_repo.delete.assert_awaited_once_with(id=12)

    async def test_delete_passenger_not_found(self, mock_repo):
        mock_repo.delete = AsyncMock(return_value=0)

        with pytest.raises(PassengerNotFound):
            await PassengerService.delete_passenger(404)
