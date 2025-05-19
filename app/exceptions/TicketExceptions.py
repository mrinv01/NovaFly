from fastapi import status, HTTPException




class TicketNotFound(HTTPException):
    def __init(self, id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Билет с id {id} не найден!"
        )

class NoTicketsForUser(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У пользователя нет билетов."
        )


