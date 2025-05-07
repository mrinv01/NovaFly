from http.client import HTTPException
from app.repositories.plane_repository import PlaneRepository
from app.schemas.plane_schemas import PlaneAddSchema, PlaneUpdateSchema, PlaneDeleteSchema
from app.exceptions.PlaneExceptions import CreateException
from fastapi import HTTPException



class PlaneService:

    @staticmethod
    async def get_all_planes():
        return await PlaneRepository.find_all()

    @staticmethod
    async def add_plane(plane_data: PlaneAddSchema):
        check = await PlaneRepository.add(**plane_data.model_dump())
        if not check:
            raise CreateException
        return check.to_dict()

    @staticmethod
    async def update_plane_info(plane_id: int, plane_data: PlaneUpdateSchema):
        await PlaneRepository.check_plane(plane_id)
        update_dict = plane_data.model_dump(exclude_none=True)
        updated_rows = await PlaneRepository.update_plane_info(plane_id, **update_dict)

        if updated_rows == 0:
            return {"message": f"Не удалось обновить самолет {plane_id}"}
        return {"message": f"Самолет {plane_id} успешно обновлён!"}

    @staticmethod
    async def delete_plane(request: PlaneDeleteSchema):
        try:
            deleted_count = await PlaneRepository.delete_by_ids(request.ids)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        return {"deleted": deleted_count}
