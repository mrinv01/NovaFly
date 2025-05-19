from fastapi import status, HTTPException

InformationNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Самолет не найден!"
)

CreateException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка при добавлении самолета"
)

class PlaneNotFound(HTTPException):
    def _init__(self, plane_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Самолет с id {plane_id} не найден!"
        )