from fastapi import HTTPException, status


class AirportNotFound(HTTPException):
    def __init__(self, airport_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Аэропорт с id {airport_id} не найден"
        )


class InformationNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет рейсов, которые соответствуют условиям поиска"
        )
