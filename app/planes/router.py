from fastapi import APIRouter, Depends
from app.planes.dao import PlaneDAO
from app.planes.schemas import PlaneSchema, PlaneSchemaAdd

router = APIRouter(prefix="/planes", tags=["Работа с самолетами"])

@router.get("/", summary="Получить все самолеты")
async def get_all_flights() -> list[PlaneSchema]:
    return await PlaneDAO.find_all()


@router.post("/add/", summary="Добавление новой модели самолета")
async def add_plane(plane: PlaneSchemaAdd) -> dict:
    check = await PlaneDAO.add(** plane.dict())
    if check:
        return {"message": "Самолет успешно добавлен!", "plane": plane}
    else:
        return {"message": "Ошибка при добавлении самолета!"}

@router.put("/update_info/", summary="Обновление информации о самолете")
async def update_info(plane: PlaneSchema ) -> dict:
    check = await PlaneDAO.update(filter_by={'id': plane.id},
                                  model = plane.model,
                                  capacity = plane.capacity)
    if check:
        return {"message": f"Информация для {plane.model} обновлена!", "plane": plane}
    else:
        return {"message": "Ошибка при изменении самолета!"}

@router.delete("/delete/{plane_id}", summary="Удаление самолета")
async def delete_plane(plane_id: int) -> dict:
    check = await PlaneDAO.delete(id=plane_id)
    if check:
        return {"message": f"Самолет с ID {plane_id} удален!"}
    else:
        return {"message": "Ошибка при удалении самолета!"}