from fastapi import APIRouter, Depends
from app.orders.schemas import OrderSchema, SAddOrder, SUpdateOrder
from app.orders.dao import OrderDAO
from app.users.dao import UserDAO
from app.exceptions.OrderExceptions import OrderExceptions

router = APIRouter(prefix = "/orders", tags = ["Работа с заказами"])

@router.get("/{user_id}", summary = "Получить все заказы пользователя")
async def get_orders_by_user(user_id: int) -> list[OrderSchema]:
    result = await OrderDAO.find_all(user_id=user_id)
    if not result:
        raise OrderExceptions.UserNotFound(user_id)
    return result

@router.post("/add/", summary = "Создание заказа для пользователя")
async def add_order(order: SAddOrder = Depends()) -> list[OrderSchema] | dict:
    user = await UserDAO.find_one_or_none_by_id(order.user_id)
    if not user:
        return {"message": f"Пользователь с id {order.user_id} не существует!"}

    check = await OrderDAO.add(** order.dict())
    if check:
        return {"message": "Заказ успешно создан!", "order_id": order.id}
    else:
        return {"message": "При создании заказа произошла ошибка!"}

@router.put("/{order_id}/status", summary = "Изменение статуса заказа")
async def update_order(order_id: int, status_data: SUpdateOrder = Depends()):
    await OrderDAO.check_order(order_id)
    updated_rows = await OrderDAO.update_status(order_id, status_data.status)
    if updated_rows == 0:
        return {"message": f"Заказ с id {order_id} не обновился."}
    return {"message": f"Статус заказа {order_id} успешно изменен на '{status_data.status}'"}



