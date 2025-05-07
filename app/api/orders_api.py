from fastapi import APIRouter, Depends, status
from app.schemas.order_schemas import OrderSchema, SUpdateOrder
from app.services.order_service import OrderService
from app.security.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["Работа с заказами"])

@router.get("/all", summary="Получить все заказы пользователя")
async def get_orders_by_user(current_user: User = Depends(get_current_user)) -> list[OrderSchema]:
    return await OrderService.get_orders_by_user(current_user.id)

@router.post("/add/", summary="Создание заказа для пользователя", status_code=status.HTTP_201_CREATED)
async def add_order(current_user: User = Depends(get_current_user)) -> dict:
    return await OrderService.add_order(current_user.id)

@router.put("/{order_id}/status", summary="Изменение статуса заказа")
async def update_order(order_id: int, status_data: SUpdateOrder = Depends()):
    return await OrderService.update_order_status(order_id, status_data)
