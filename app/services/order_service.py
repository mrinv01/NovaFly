from app.repositories.order_repository import OrderRepository
from app.exceptions.OrderExceptions import OrderNotFound
from app.schemas.order_schemas import SUpdateOrder


class OrderService:

    @staticmethod
    async def get_orders_by_user(user_id: int):
        result = await OrderRepository.find_all(user_id=user_id)
        if not result:
            raise OrderNotFound(user_id)
        return result

    @staticmethod
    async def add_order(user_id: int):
        check = await OrderRepository.add(user_id=user_id)
        if check:
            return {"message": "Заказ успешно создан!", "order_id": check.id}
        return {"message": "При создании заказа произошла ошибка!"}

    @staticmethod
    async def update_order_status(order_id: int, status_data: SUpdateOrder):
        await OrderRepository.check_order(order_id)
        updated_rows = await OrderRepository.update_status(order_id, status_data.status)
        if updated_rows == 0:
            return {"message": f"Заказ с id {order_id} не обновился."}
        return {"message": f"Статус заказа {order_id} успешно изменен на '{status_data.status}'"}
