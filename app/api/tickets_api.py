from fastapi import APIRouter, Depends
from app.schemas.ticket_schemas import TicketSchema, SAddTicket, SUpdateTicket
from app.security.deps import get_current_admin_user, get_current_user
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Работа с билетами"])

@router.get("/", summary="Получение всех билетов для пользователя")
async def get_all_tickets(current_user=Depends(get_current_user)) -> list[TicketSchema]:
    return await TicketService.get_user_tickets(current_user.id)

@router.get("/{user_id}", summary="Получение билетов конкретного пользователя (для админа)")
async def get_ticket_by_user(user_id: int, current_user=Depends(get_current_admin_user)) -> list[TicketSchema]:
    return await TicketService.get_user_tickets(user_id)

@router.post("/add", summary="Создание билета")
async def add_ticket(ticket: SAddTicket = Depends(), current_user=Depends(get_current_user)):
    return await TicketService.add_ticket(ticket, current_user.id)

@router.put("/{ticket_id}", summary="Изменение билета (только админ)")
async def update_ticket(ticket_id: int, ticket_data: SUpdateTicket = Depends(),
                        current_user=Depends(get_current_admin_user)):
    return await TicketService.update_ticket(ticket_id, ticket_data)

@router.delete("/delete/{ticket_id}", summary="Удаление билета")
async def delete_ticket(ticket_id: int):
    return await TicketService.delete_ticket(ticket_id)
