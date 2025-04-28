from fastapi import APIRouter, Depends
from app.tickets.schemas import TicketSchema, SAddTicket, SUpdateTicket
from app.tickets.dao import TicketDAO
from app.orders.dao import OrderDAO
from app.exceptions.TicketExceptions import TicketExceptions

router = APIRouter(prefix="/tickets", tags=["Работа с билетами"])

@router.get("/{order_id}/", summary = "Получение всех билетов из заказа")
async def get_all_tickets(order_id: int) -> list[TicketSchema] | dict:
    await OrderDAO.check_order(order_id)
    tickets = await TicketDAO.find_all(order_id=order_id)
    if not tickets:
        return {"message": "В этом зкаказе нет билетов!"}
    return tickets

@router.post("/{order_id}/add", summary = "Добавление билета к заказу")
async def add_ticket(order_id: int, ticket: SAddTicket):
    await OrderDAO.check_order(order_id)
    ticket_dict = ticket.dict()
    ticket_dict["order_id"] = order_id
    new_ticket = await TicketDAO.add(**ticket_dict)
    if new_ticket:
        return {"message": "Билет успешно добавлен!", "ticket": new_ticket}
    else:
        return {"message": "Ошибка при добавлении билета!"}

@router.put("/{order_id}/{ticket_id}", summary="Изменение билета в заказе")
async def update_ticket(order_id: int, ticket_id: int, ticket_data: SUpdateTicket = Depends()):
    await OrderDAO.check_order(order_id)
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


