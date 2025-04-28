from fastapi import status, HTTPException


class OrderExceptions(BaseException):
    def OrderNotFound(id: int):
        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail= f"У пользователя с id {id} нет заказов!")
        return exception

    def UserNotFound(id: int):
        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail= f"Пользователь с id {id} не найден!")
        return exception
