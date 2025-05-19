import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.plane_service import PlaneService
from app.schemas.plane_schemas import PlaneAddSchema, PlaneUpdateSchema, PlaneDeleteSchema
from app.exceptions.PlaneExceptions import CreateException
from fastapi import HTTPException


@pytest.mark.asyncio
@patch("app.services.plane_service.PlaneRepository")
class TestPlaneService:

    async def test_get_all_planes(self, mock_repo):
        mock_repo.find_all = AsyncMock(return_value=[{"id": 1, "model": "A320", "capacity": 180}])

        result = await PlaneService.get_all_planes()

        assert result == [{"id": 1, "model": "A320", "capacity": 180}]
        mock_repo.find_all.assert_awaited_once()

    async def test_add_plane_success(self, mock_repo):
        plane_data = PlaneAddSchema(model="Boeing 737", capacity=160)

        mock_plane = MagicMock()
        mock_plane.to_dict.return_value = {"id": 1, "model": "Boeing 737", "capacity": 160}
        mock_repo.add = AsyncMock(return_value=mock_plane)

        result = await PlaneService.add_plane(plane_data)

        mock_repo.add.assert_awaited_once_with(**plane_data.model_dump())
        assert result["model"] == "Boeing 737"
        assert result["capacity"] == 160
        assert result["id"] == 1


    async def test_add_plane_failure(self, mock_repo):
        plane_data = PlaneAddSchema(model="SSJ-100", capacity=100)
        mock_repo.add = AsyncMock(return_value=None)

        with pytest.raises(CreateException.__class__):
            await PlaneService.add_plane(plane_data)

    async def test_update_plane_info_success(self, mock_repo):
        mock_repo.check_plane = AsyncMock()
        mock_repo.update_plane_info = AsyncMock(return_value=1)

        plane_data = PlaneUpdateSchema(model="Airbus A350")
        result = await PlaneService.update_plane_info(5, plane_data)

        assert result["message"] == "Самолет 5 успешно обновлён!"
        mock_repo.update_plane_info.assert_awaited_once_with(5, model="Airbus A350")

    async def test_update_plane_info_not_updated(self, mock_repo):
        mock_repo.check_plane = AsyncMock()
        mock_repo.update_plane_info = AsyncMock(return_value=0)

        plane_data = PlaneUpdateSchema(capacity=250)
        result = await PlaneService.update_plane_info(2, plane_data)

        assert result["message"] == "Не удалось обновить самолет 2"

    async def test_delete_plane_success(self, mock_repo):
        mock_repo.delete_by_ids = AsyncMock(return_value=2)
        request = PlaneDeleteSchema(ids=[1, 2])

        result = await PlaneService.delete_plane(request)

        assert result["deleted"] == 2
        mock_repo.delete_by_ids.assert_awaited_once_with([1, 2])

    async def test_delete_plane_value_error(self, mock_repo):
        mock_repo.delete_by_ids = AsyncMock(side_effect=ValueError("Некорректный ID"))

        request = PlaneDeleteSchema(ids=[-1])
        with pytest.raises(HTTPException) as exc_info:
            await PlaneService.delete_plane(request)

        assert exc_info.value.status_code == 400
        assert "Некорректный ID" in exc_info.value.detail
