from fastapi import APIRouter, Depends
from app.schemas.flight_schemas import FlightSchema, SAddFlight, SUpdateFlight
from app.schemas.request_body_flight import RequestBodyFlight
from app.services.flight_service import FlightService
from app.security.deps import get_current_admin_user
from app.models.user import User

router = APIRouter(prefix="/flights", tags=["Работа с рейсами"])

@router.get("/", summary="Получить все рейсы")
async def get_all_flights() -> list[FlightSchema]:
    return await FlightService.get_all_flights()

@router.get("/filter/by", summary="Получение рейсов согласно фильтру")
async def get_flight_by_filter(request_body: RequestBodyFlight = Depends()) -> list[FlightSchema]:
    return await FlightService.get_flight_by_filter(request_body)

@router.get("/{id}", summary="Получить один рейс по id")
async def get_flight_by_id(id: int) -> FlightSchema | dict:
    return await FlightService.get_flight_by_id(id)

@router.post("/add/", summary="Создать новый рейс")
async def add_flight(flight: SAddFlight = Depends(),
                     user: User = Depends(get_current_admin_user)) -> dict:
    return await FlightService.add_flight(flight)

@router.put("/{flight_id}", summary="Обновление информации о рейсе")
async def update_flight(flight_id: int, update_data: SUpdateFlight = Depends(),
                        user: User = Depends(get_current_admin_user)):
    return await FlightService.update_flight(flight_id, update_data)
