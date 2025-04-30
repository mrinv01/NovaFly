from fastapi import APIRouter, Depends
from app.repositories.flight_repository import FlightDAO
from app.schemas.request_body_flight import RequestBodyFlight
from app.schemas.flight_schemas import FlightSchema, SAddFlight, SUpdateFlight
from app.exceptions.FlightExceptions import InformationNotFoundException
from app.security.deps import get_current_admin_user
from app.models.user import User
from app.repositories.plane_repository import PlaneRepository
from app.repositories.airport_repository import AirportRepository


router = APIRouter(prefix="/flights", tags=["Работа с рейсами"])

@router.get("/", summary="Получить все рейсы")
async def get_all_flights() -> list[FlightSchema]:
    return await FlightDAO.find_all()

@router.get("/filter/by", summary="Получение рейсов согласно фильтру")
async def get_flight_by_filter(request_body: RequestBodyFlight = Depends()) -> list[FlightSchema]:
    result = await FlightDAO.find_all(**request_body.to_dict())
    if not result:
        raise InformationNotFoundException
    return result

@router.get("/{id}", summary="Получить один рейс по id")
async def get_flight_by_id(id: int) -> FlightSchema | dict:
    result = await FlightDAO.find_one_or_none_by_id(id)
    if result is None:
        raise InformationNotFoundException
    return result

@router.post("/add/", summary="Создать новый рейс")
async def add_flight(flight: SAddFlight = Depends(), user: User = Depends(get_current_admin_user)) -> dict:
    await PlaneRepository.check_plane(flight.plane_id)
    await AirportRepository.check_airport(flight.departure_from)
    await AirportRepository.check_airport(flight.arrival_to)

    check = await FlightDAO.add(** flight.dict())
    if check:
        return {"message": "Рейс успешно создан!", "flight": flight}
    else:
        return {"message": "При создании рейса произошла ошибка!"}

@router.put("/{flight_id}", summary="Обновление информации о рейсе")
async def update_flight(flight_id: int, update_data: SUpdateFlight=Depends(), user: User = Depends(get_current_admin_user)):
    update_dict = update_data.dict(exclude_none=True)
    updated_rows = await FlightDAO.update_flight_info(flight_id, **update_dict)
    if updated_rows == 0:
        raise InformationNotFoundException
    return {"message": f"Рейс {flight_id} успешно обновлён"}


