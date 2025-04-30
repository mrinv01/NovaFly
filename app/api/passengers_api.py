from fastapi import APIRouter, Depends
from app.schemas.passenger_schemas import SCreatePassenger, SUpdatePassenger, SPassengerOut
from app.repositories.passenger_repository import PassengerDAO
from app.schemas.request_body_passenger import RBPassenger
from app.exceptions.PassengerExceptions import PassengerExceptions, InformationNotFoundException

router = APIRouter(prefix="/passengers", tags=["Работа с пассажирами"])

@router.post("/add/", summary="Создать пассажира", response_model=SPassengerOut)
async def create_passenger(passenger_data: SCreatePassenger = Depends()):
    passenger = await PassengerDAO.add(**passenger_data.dict())
    return passenger

@router.get("/", summary="Получить всех пассажиров", response_model=list[SPassengerOut])
async def get_all_passengers():
    passengers = await PassengerDAO.find_all()
    return passengers

@router.get("/filter/by", summary="Получение пассажиров по фильтру")
async def get_passengers_by_filter(request_body: RBPassenger = Depends()) -> list[SPassengerOut]:
    result = await PassengerDAO.find_all(**request_body.to_dict())
    if not result:
        raise InformationNotFoundException
    return result

@router.get("/{id}", summary="Получить одного пассажира по id")
async def get_flight_by_id(id: int) -> SPassengerOut | dict:
    result = await PassengerDAO.find_one_or_none_by_id(id)
    if result is None:
        raise InformationNotFoundException
    return result

@router.put("/{passenger_id}", summary="Обновить данные пассажира")
async def update_passenger(passenger_id: int, passenger_data: SUpdatePassenger = Depends()):
    update_data = passenger_data.dict(exclude_none=True)
    updated_rows = await PassengerDAO.update({"id": passenger_id}, **update_data)
    if updated_rows == 0:
        return {"message": f"Пассажир с id {passenger_id} не найден или не обновился."}
    return {"message": f"Данные пассажира {passenger_id} успешно обновлены."}

@router.delete("/{passenger_id}", summary="Удалить пассажира")
async def delete_passenger(passenger_id: int):
    deleted_rows = await PassengerDAO.delete(id=passenger_id)
    if deleted_rows == 0:
        raise PassengerExceptions.PassengerNotFound(passenger_id)
    return {"message": f"Пассажир {passenger_id} успешно удален."}
