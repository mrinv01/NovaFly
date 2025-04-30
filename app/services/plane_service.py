from app.repositories.plane_repository import PlaneRepository
from app.schemas.plane_schemas import PlaneSchemaAdd, PlaneSchemaUpdate


class PlaneService:

    @staticmethod
    async def get_all_planes():
        return await PlaneRepository.find_all()

    @staticmethod
    async def add_plane(plane_data: PlaneSchemaAdd):
        check = await PlaneRepository.add(**plane_data.model_dump())
        if check:
            return {"message": "Самолет успешно добавлен!", "plane": plane_data}
        return {"message": "Ошибка при добавлении самолета!"}

    @staticmethod
    async def update_plane_info(plane_id: int, plane_data: PlaneSchemaUpdate):
        await PlaneRepository.check_plane(plane_id)
        update_dict = plane_data.model_dump(exclude_none=True)
        updated_rows = await PlaneRepository.update_plane_info(plane_id, **update_dict)

        if updated_rows == 0:
            return {"message": f"Не удалось обновить самолет {plane_id}"}
        return {"message": f"Самолет {plane_id} успешно обновлён!"}

    @staticmethod
    async def delete_plane(plane_id: int):
        check = await PlaneRepository.delete(id=plane_id)
        if check:
            return {"message": f"Самолет с ID {plane_id} удален!"}
        return {"message": "Ошибка при удалении самолета!"}
