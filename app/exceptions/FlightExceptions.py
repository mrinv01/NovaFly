from fastapi import HTTPException, status

class InformationNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет рейсов, которые соответствуют условиям поиска"
        )

class NoFlights(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет рейсов для отображения"
        )

class FlightNotFound(HTTPException):
    def __init__(self, flight_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рейс с id {flight_id} не найден!"
        )
