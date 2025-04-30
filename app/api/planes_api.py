from fastapi import APIRouter, Depends
from app.schemas.plane_schemas import PlaneSchema, PlaneSchemaAdd, PlaneSchemaUpdate
from app.security.deps import get_current_admin_user
from app.models import User
from app.services.plane_service import PlaneService

router = APIRouter(prefix="/planes", tags=["Работа с самолетами"])

@router.get("/", summary="Получить все самолеты")
async def get_all_planes(user: User = Depends(get_current_admin_user)) -> list[PlaneSchema]:
    return await PlaneService.get_all_planes()

@router.post("/add/", summary="Добавление новой модели самолета")
async def add_plane(plane: PlaneSchemaAdd, user: User = Depends(get_current_admin_user)) -> dict:
    return await PlaneService.add_plane(plane)

@router.put("/update_info/", summary="Обновление информации о самолете")
async def update_info(plane_id: int, plane: PlaneSchemaUpdate = Depends(),
                      user: User = Depends(get_current_admin_user)) -> dict:
    return await PlaneService.update_plane_info(plane_id, plane)

@router.delete("/delete/{plane_id}", summary="Удаление самолета")
async def delete_plane(plane_id: int, user: User = Depends(get_current_admin_user)) -> dict:
    return await PlaneService.delete_plane(plane_id)
