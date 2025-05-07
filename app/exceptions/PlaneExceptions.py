from fastapi import status, HTTPException

InformationNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Самолет не найден!"
)

CreateException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка при создании объекта"
)

class PlaneExceptions(HTTPException):
    def PlaneNotFound(plane_id: int):
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Самолет с id {plane_id} не найден!"
        )
        return exception