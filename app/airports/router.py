from fastapi import APIRouter, Depends, Path, Query
from app.airports.schemas import SAirportCreate, SAirportOut, SAirportUpdate
from app.airports.dao import AirportDAO
from app.exceptions.AirportExceptions import AirportExceptions, InformationNotFoundException

router = APIRouter(prefix="/airports", tags=["Работа с аэропортами"])

@router.post("/", summary="Создать аэропорт", response_model=SAirportOut)
async def create_airport(airport: SAirportCreate):
    created_airport = await AirportDAO.add(**airport.dict())
    return created_airport

@router.get("/", summary="Получить все аэропорты", response_model=list[SAirportOut])
async def get_all_airports():
    airports = await AirportDAO.find_all()
    return airports

@router.get("/{airport_id}", summary="Получить аэропорт по ID", response_model=SAirportOut)
async def get_airport_by_id(airport_id: int = Path(..., title="ID аэропорта")):
    airport = await AirportDAO.find_one_or_none_by_id(airport_id)
    if not airport:
        raise AirportExceptions.AirportNotFound(airport_id)
    return airport

@router.get("/search/by-city", summary="Поиск аэропортов по городу", response_model=list[SAirportOut])
async def search_airports_by_city(city: str = Query(..., title="Часть названия города")):
    airports = await AirportDAO.find_by_city(city)
    if not airports:
        raise InformationNotFoundException
    return airports

@router.put("/{airport_id}", summary="Обновить данные аэропорта", response_model=SAirportOut)
async def update_airport(airport_id: int, airport_update: SAirportUpdate):
    updated_fields = airport_update.dict(exclude_none=True)
    updated_rows = await AirportDAO.update({"id": airport_id}, **updated_fields)
    if updated_rows == 0:
        raise AirportExceptions.AirportNotFound(airport_id)
    updated_airport = await AirportDAO.find_one_or_none_by_id(airport_id)
    return updated_airport

@router.delete("/{airport_id}", summary="Удалить аэропорт")
async def delete_airport(airport_id: int):
    deleted_rows = await AirportDAO.delete(id=airport_id)
    if deleted_rows == 0:
        raise AirportExceptions.AirportNotFound(airport_id)
    return {"message": f"Аэропорт с id {airport_id} успешно удалён"}
