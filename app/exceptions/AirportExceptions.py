from fastapi import status, HTTPException

InformationNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Нет рейсов, которые соответствуют условиям поиска"
)

class AirportExceptions(BaseException):
    def AirportNotFound(id: int):
        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail= f"Аэропорт с id {id} не найден!")
        return exception