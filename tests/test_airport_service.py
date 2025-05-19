import pytest
from unittest.mock import AsyncMock, patch

from app.services.airport_service import AirportService
from app.schemas.airport_schemas import SAirportCreate, SAirportUpdate
from app.exceptions.AirportExceptions import AirportNotFound, InformationNotFoundException

@pytest.mark.asyncio
@patch("app.services.airport_service.AirportRepository")
class TestAirportService:

    async def test_create_airport(self, mock_repo):
        data = SAirportCreate(city="Москва", airport_code="SVO")
        mock_repo.add = AsyncMock(return_value={"id": 1, **data.model_dump()})

        result = await AirportService.create_airport(data)

        mock_repo.add.assert_awaited_once_with(**data.model_dump())
        assert result["city"] == "Москва"
        assert result["airport_code"] == "SVO"

    async def test_get_all_airports(self, mock_repo):
        mock_repo.find_all = AsyncMock(return_value=[{"id": 1, "city": "Москва", "airport_code": "SVO"}])

        result = await AirportService.get_all_airports()

        mock_repo.find_all.assert_awaited_once()
        assert isinstance(result, list)
        assert result[0]["city"] == "Москва"

    async def test_get_airport_by_id_found(self, mock_repo):
        mock_repo.find_one_or_none_by_id = AsyncMock(return_value={"id": 1, "city": "Москва", "airport_code": "SVO"})

        result = await AirportService.get_airport_by_id(1)

        mock_repo.find_one_or_none_by_id.assert_awaited_once_with(1)
        assert result["id"] == 1

    async def test_get_airport_by_id_not_found(self, mock_repo):
        mock_repo.find_one_or_none_by_id = AsyncMock(return_value=None)

        with pytest.raises(AirportNotFound) as exc_info:
            await AirportService.get_airport_by_id(99)
        assert "Аэропорт с id 99 не найден" in str(exc_info.value)

    async def test_search_by_city(self, mock_repo):
        mock_repo.find_by_city = AsyncMock(return_value=[{"id": 1, "city": "Москва", "airport_code": "SVO"}])

        result = await AirportService.search_by_city("Москва")

        mock_repo.find_by_city.assert_awaited_once_with("Москва")
        assert result[0]["city"] == "Москва"

    async def test_search_by_city_not_found(self, mock_repo):
        mock_repo.find_by_city = AsyncMock(return_value=[])

        with pytest.raises(InformationNotFoundException) as exc_info:
            await AirportService.search_by_city("НеизвестныйГород")
        assert "Нет рейсов, которые соответствуют условиям поиска" in str(exc_info.value)

    async def test_update_airport_success(self, mock_repo):
        mock_repo.update = AsyncMock(return_value=1)
        mock_repo.find_one_or_none_by_id = AsyncMock(return_value={"id": 1, "city": "Казань", "airport_code": "KZN"})

        data = SAirportUpdate(city="Казань")
        result = await AirportService.update_airport(1, data)

        mock_repo.update.assert_awaited_once_with({"id": 1}, city="Казань")
        mock_repo.find_one_or_none_by_id.assert_awaited_with(1)
        assert result["city"] == "Казань"

    async def test_update_airport_not_found(self, mock_repo_cls):
        mock_repo = mock_repo_cls
        mock_repo.find_one_or_none_by_id = AsyncMock(return_value=None)
        mock_repo.update = AsyncMock(return_value=0)

        data = SAirportUpdate(city="Казань")

        with pytest.raises(AirportNotFound) as exc_info:
            await AirportService.update_airport(999, data)

        assert "Аэропорт с id 999 не найден" in str(exc_info.value)

    async def test_delete_airport_success(self, mock_repo):
        mock_repo.delete = AsyncMock(return_value=1)

        result = await AirportService.delete_airport(1)

        mock_repo.delete.assert_awaited_once_with(id=1)
        assert result["message"] == "Аэропорт с id 1 успешно удалён"

    async def test_delete_airport_not_found(self, mock_repo):
        mock_repo.delete = AsyncMock(return_value=0)

        with pytest.raises(AirportNotFound) as exc_info:
            await AirportService.delete_airport(999)
        assert "Аэропорт с id 999 не найден" in str(exc_info.value)
