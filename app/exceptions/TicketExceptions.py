from fastapi import status, HTTPException


class TicketExceptions(BaseException):
    def TicketNotFound(id: int):
        exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail= f"Билет с id {id} не найден!")
        return exception

    NoTicketsForUser = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='У пользователя нет билетов!')



