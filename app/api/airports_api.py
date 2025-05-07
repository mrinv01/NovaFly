from fastapi import APIRouter, Depends, Path, Query, status
from app.schemas.airport_schemas import SAirportCreate, SAirportOut, SAirportUpdate
from app.services.airport_service import AirportService
from app.security.deps import get_current_admin_user
from app.models import User

router = APIRouter(prefix="/airports", tags=["Работа с аэропортами"])

@router.post("/", summary="Создать аэропорт", response_model=SAirportOut, status_code=status.HTTP_201_CREATED)
async def create_airport(airport: SAirportCreate, user: User = Depends(get_current_admin_user)):
    return await AirportService.create_airport(airport)

@router.get("/", summary="Получить все аэропорты", response_model=list[SAirportOut])
async def get_all_airports():
    return await AirportService.get_all_airports()

@router.get("/{airport_id}", summary="Получить аэропорт по ID", response_model=SAirportOut)
async def get_airport_by_id(airport_id: int = Path(...)):
    return await AirportService.get_airport_by_id(airport_id)

@router.get("/search/by-city", summary="Поиск аэропортов по городу", response_model=list[SAirportOut])
async def search_airports_by_city(city: str = Query(...)):
    return await AirportService.search_by_city(city)

@router.put("/{airport_id}", summary="Обновить данные аэропорта", response_model=SAirportOut)
async def update_airport(airport_id: int, airport_update: SAirportUpdate, user: User = Depends(get_current_admin_user)):
    return await AirportService.update_airport(airport_id, airport_update)

@router.delete("/{airport_id}", summary="Удалить аэропорт")
async def delete_airport(airport_id: int, user: User = Depends(get_current_admin_user)):
    return await AirportService.delete_airport(airport_id)
