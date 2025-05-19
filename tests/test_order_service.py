import pytest
from unittest.mock import AsyncMock, patch

from app.services.order_service import OrderService
from app.schemas.order_schemas import SUpdateOrder
from app.exceptions.OrderExceptions import OrderNotFound


@pytest.mark.asyncio
@patch("app.services.order_service.OrderRepository")
class TestOrderService:

    async def test_get_orders_by_user_success(self, mock_repo):
        mock_repo.find_all = AsyncMock(return_value=[{"id": 1, "status": "Создан"}])

        result = await OrderService.get_orders_by_user(1)

        mock_repo.find_all.assert_awaited_once_with(user_id=1)
        assert isinstance(result, list)
        assert result[0]["status"] == "Создан"

    async def test_get_orders_by_user_not_found(self, mock_repo):
        mock_repo.find_all = AsyncMock(return_value=[])

        with pytest.raises(OrderNotFound):
            await OrderService.get_orders_by_user(999)

    async def test_add_order_success(self, mock_repo):
        mock_order = type("MockOrder", (object,), {"id": 42})
        mock_repo.add = AsyncMock(return_value=mock_order)

        result = await OrderService.add_order(1)

        mock_repo.add.assert_awaited_once_with(user_id=1)
        assert result["message"] == "Заказ успешно создан!"
        assert result["order_id"] == 42

    async def test_add_order_failure(self, mock_repo):
        mock_repo.add = AsyncMock(return_value=None)

        result = await OrderService.add_order(1)

        assert result["message"] == "При создании заказа произошла ошибка!"

    async def test_update_order_status_success(self, mock_repo):
        mock_repo.check_order = AsyncMock()
        mock_repo.update_status = AsyncMock(return_value=1)

        status_data = SUpdateOrder(status="Оплачен")

        result = await OrderService.update_order_status(10, status_data)

        mock_repo.check_order.assert_awaited_once_with(10)
        mock_repo.update_status.assert_awaited_once_with(10, "Оплачен")
        assert result["message"] == "Статус заказа 10 успешно изменен на 'Оплачен'"

    async def test_update_order_status_no_update(self, mock_repo):
        mock_repo.check_order = AsyncMock()
        mock_repo.update_status = AsyncMock(return_value=0)

        status_data = SUpdateOrder(status="Отменён")

        result = await OrderService.update_order_status(999, status_data)

        assert result["message"] == "Заказ с id 999 не обновился."
