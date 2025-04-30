from fastapi import APIRouter, Depends
from app.schemas.ticket_schemas import TicketSchema, SAddTicket, SUpdateTicket
from app.repositories.ticket_repository import TicketDAO
from app.exceptions.TicketExceptions import TicketExceptions
from app.security.deps import get_current_admin_user, get_current_user

router = APIRouter(prefix="/tickets", tags=["Работа с билетами"])

@router.get("/", summary = "Получение всех билетов для пользователя")
async def get_all_tickets(current_user = Depends(get_current_user)) -> list[TicketSchema]:
    tickets = await TicketDAO.find_all(user_id=current_user.id)
    if not tickets:
        raise TicketExceptions.NoTicketsForUser
    return tickets

@router.get("/{user_id}", summary = "Получение билетов конкретного пользователя (для админа)")
async def get_ticket_by_user(user_id: int, current_user = Depends(get_current_admin_user)) -> list[TicketSchema]:
    tickets = await TicketDAO.find_all(user_id=user_id)
    if not tickets:
        raise TicketExceptions.NoTicketsForUser
    return tickets

@router.post("/add", summary = "Создание билета")
async def add_ticket(ticket: SAddTicket, current_user = Depends(get_current_user)):
    ticket_dict = ticket.model_dump()
    ticket_dict["user_id"] = current_user.id
    new_ticket = await TicketDAO.add(**ticket_dict)
    if new_ticket:
        return {"message": "Билет успешно добавлен!", "ticket": new_ticket}
    else:
        return {"message": "Ошибка при добавлении билета!"}

@router.put("/{ticket_id}", summary="Изменение билета (только админ)")
async def update_ticket(ticket_id: int, ticket_data: SUpdateTicket = Depends(),
                        current_user = Depends(get_current_admin_user)):
    await TicketDAO.check_ticket(ticket_id)
    update_dict = ticket_data.dict(exclude_none=True)

    updated_rows = await TicketDAO.update_ticket_info(ticket_id, **update_dict)

    if updated_rows == 0:
        return {"message": f"Не удалось обновить билет {ticket_id}"}

    return {"message": f"Билет {ticket_id} успешно обновлён!"}

@router.delete("/delete/{ticket_id}", summary="Удаление билета")
async def delete_plane(ticket_id: int) -> dict:
    check = await TicketDAO.delete(id=ticket_id)
    if check:
        return {"message": f"Билет с id {ticket_id} удален!"}
    else:
        raise TicketExceptions.TicketNotFound(ticket_id)


