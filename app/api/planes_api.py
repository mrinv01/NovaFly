from fastapi import APIRouter, Depends
from app.repositories.plane_repository import PlaneRepository
from app.schemas.plane_schemas import PlaneSchema, PlaneSchemaAdd, PlaneSchemaUpdate
from app.security.deps import get_current_admin_user
from app.models import User

router = APIRouter(prefix="/planes", tags=["Работа с самолетами"])

@router.get("/", summary="Получить все самолеты")
async def get_all_flights(user: User = Depends(get_current_admin_user)) -> list[PlaneSchema]:
    return await PlaneRepository.find_all()


@router.post("/add/", summary="Добавление новой модели самолета")
async def add_plane(plane: PlaneSchemaAdd, user: User = Depends(get_current_admin_user)) -> dict:
    check = await PlaneRepository.add(** plane.dict())
    if check:
        return {"message": "Самолет успешно добавлен!", "plane": plane}
    else:
        return {"message": "Ошибка при добавлении самолета!"}

@router.put("/update_info/", summary="Обновление информации о самолете")
async def update_info(plane_id: int, plane: PlaneSchemaUpdate = Depends(), user: User = Depends(get_current_admin_user)) -> dict:
    await PlaneRepository.check_plane(plane_id)
    update_dict = plane.dict(exclude_none=True)

    updated_rows = await PlaneRepository.update_plane_info(plane_id, **update_dict)

    if updated_rows == 0:
        return {"message": f"Не удалось обновить самолет {plane_id}"}

    return {"message": f"Самолет {plane_id} успешно обновлён!"}

@router.delete("/delete/{plane_id}", summary="Удаление самолета")
async def delete_plane(plane_id: int, user: User = Depends(get_current_admin_user)) -> dict:
    check = await PlaneRepository.delete(id=plane_id)
    if check:
        return {"message": f"Самолет с ID {plane_id} удален!"}
    else:
        return {"message": "Ошибка при удалении самолета!"}