from fastapi import status, HTTPException

InformationNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Нет рейсов, которые соответствуют условиям поиска"
)

NoFlights = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Нет рейсов для отображения"
)

class FlightExceptions(HTTPException):
    def FlightNotFound(flight_id: int):
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Рейс с id {flight_id} не найден!"
        )
        return exception