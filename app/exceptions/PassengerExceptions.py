from fastapi import status, HTTPException


class InformationNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Нет пассажиров, которые соответствуют условиям поиска"
        )

class PassengerNotFound(HTTPException):
    def __init__(self, id: int):
        super().__init__ (
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Пассажир с id {id} не найден!"
        )