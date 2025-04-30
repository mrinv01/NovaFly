from fastapi import APIRouter, Depends
from app.schemas.order_schemas import OrderSchema, SUpdateOrder
from app.repositories.order_repository import OrderDAO
from app.exceptions.OrderExceptions import OrderExceptions
from app.security.deps import get_current_user


router = APIRouter(prefix = "/orders", tags = ["Работа с заказами"])

@router.get("/all", summary = "Получить все заказы пользователя")
async def get_orders_by_user(current_user = Depends(get_current_user)) -> list[OrderSchema]:
    user_id = int(current_user.id)
    result = await OrderDAO.find_all(user_id=user_id)
    if not result:
        raise OrderExceptions.OrderNotFound(user_id)
    return result

@router.post("/add/", summary = "Создание заказа для пользователя")
async def add_order(current_user = Depends(get_current_user)) -> list[OrderSchema] | dict:
    check = await OrderDAO.add(user_id=current_user.id)
    if check:
        return {"message": "Заказ успешно создан!", "order_id": check.id}
    else:
        return {"message": "При создании заказа произошла ошибка!"}

@router.put("/{order_id}/status", summary = "Изменение статуса заказа")
async def update_order(order_id: int, status_data: SUpdateOrder = Depends()):
    await OrderDAO.check_order(order_id)
    updated_rows = await OrderDAO.update_status(order_id, status_data.status)
    if updated_rows == 0:
        return {"message": f"Заказ с id {order_id} не обновился."}
    return {"message": f"Статус заказа {order_id} успешно изменен на '{status_data.status}'"}



