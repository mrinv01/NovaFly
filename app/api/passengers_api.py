from fastapi import APIRouter, Depends, status
from app.schemas.passenger_schemas import SCreatePassenger, SUpdatePassenger, SPassengerOut
from app.schemas.request_body_passenger import RBPassenger
from app.services.passenger_service import PassengerService

router = APIRouter(prefix="/passengers", tags=["Работа с пассажирами"])

@router.post("/add/", summary="Создать пассажира", response_model=SPassengerOut, status_code=status.HTTP_201_CREATED)
async def create_passenger(passenger_data: SCreatePassenger = Depends()):
    return await PassengerService.create_passenger(passenger_data)

@router.get("/", summary="Получить всех пассажиров", response_model=list[SPassengerOut])
async def get_all_passengers():
    return await PassengerService.get_all_passengers()

@router.get("/filter/by", summary="Получение пассажиров по фильтру")
async def get_passengers_by_filter(request_body: RBPassenger = Depends()) -> list[SPassengerOut]:
    return await PassengerService.get_passengers_by_filter(request_body)

@router.get("/{id}", summary="Получить одного пассажира по id")
async def get_passenger_by_id(id: int) -> SPassengerOut | dict:
    return await PassengerService.get_passenger_by_id(id)

@router.put("/{passenger_id}", summary="Обновить данные пассажира")
async def update_passenger(passenger_id: int, passenger_data: SUpdatePassenger = Depends()):
    return await PassengerService.update_passenger(passenger_id, passenger_data)

@router.delete("/{passenger_id}", summary="Удалить пассажира")
async def delete_passenger(passenger_id: int):
    return await PassengerService.delete_passenger(passenger_id)
