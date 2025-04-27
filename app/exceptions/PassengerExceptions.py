from fastapi import status, HTTPException


InformationNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Нет пассажиров, которые соответствуют условиям поиска"
)

class PassengerExceptions(BaseException):
    def PassengerNotFound(id: int):
        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail= f"Пассажир с id {id} не найден!")
        return exception