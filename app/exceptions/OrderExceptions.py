from fastapi import HTTPException, status

class OrderNotFound(HTTPException):
    def __init__(self, id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"У пользователя с id {id} нет заказов!"
        )

class UserNotFound(HTTPException):
    def __init__(self, id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с id {id} не найден!"
        )
