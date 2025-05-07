from fastapi import APIRouter, Depends, status
from app.schemas.plane_schemas import PlaneSchema, PlaneAddSchema, PlaneUpdateSchema, PlaneDeleteSchema
from app.security.deps import get_current_admin_user
from app.models import User
from app.services.plane_service import PlaneService

router = APIRouter(prefix="/planes", tags=["Работа с самолетами"])

@router.get("/", summary="Получить все самолеты")
async def get_all_planes(user: User = Depends(get_current_admin_user)) -> list[PlaneSchema]:
    return await PlaneService.get_all_planes()

@router.post("/add/", summary="Добавление новой модели самолета", status_code=status.HTTP_201_CREATED)
async def add_plane(plane: PlaneAddSchema, user: User = Depends(get_current_admin_user)) -> dict:
    return await PlaneService.add_plane(plane)

@router.put("/update_info/", summary="Обновление информации о самолете")
async def update_info(plane_id: int, plane: PlaneUpdateSchema = Depends(),
                      user: User = Depends(get_current_admin_user)) -> dict:
    return await PlaneService.update_plane_info(plane_id, plane)

@router.delete("/delete/", summary="Удаление самолета(ов)")
async def delete_plane(request: PlaneDeleteSchema, user: User = Depends(get_current_admin_user)) -> dict:
    return await PlaneService.delete_plane(request)
