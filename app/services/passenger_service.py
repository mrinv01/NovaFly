from app.repositories.passenger_repository import PassengerRepository
from app.schemas.passenger_schemas import SCreatePassenger, SUpdatePassenger
from app.schemas.request_body_passenger import RBPassenger
from app.exceptions.PassengerExceptions import PassengerNotFound, InformationNotFound


class PassengerService:

    @staticmethod
    async def create_passenger(passenger_data: SCreatePassenger):
        return await PassengerRepository.add(**passenger_data.model_dump())

    @staticmethod
    async def get_all_passengers():
        return await PassengerRepository.find_all()

    @staticmethod
    async def get_passengers_by_filter(request_body: RBPassenger):
        result = await PassengerRepository.find_all(**request_body.to_dict())
        if not result:
            raise InformationNotFound
        return result

    @staticmethod
    async def get_passenger_by_id(passenger_id: int):
        result = await PassengerRepository.find_one_or_none_by_id(passenger_id)
        if result is None:
            raise InformationNotFound
        return result

    @staticmethod
    async def update_passenger(passenger_id: int, update_data: SUpdatePassenger):
        update_dict = update_data.model_dump(exclude_none=True)
        updated_rows = await PassengerRepository.update({"id": passenger_id}, **update_dict)
        if updated_rows == 0:
            return {"message": f"Пассажир с id {passenger_id} не найден или не обновился."}
        return {"message": f"Данные пассажира {passenger_id} успешно обновлены."}

    @staticmethod
    async def delete_passenger(passenger_id: int):
        deleted_rows = await PassengerRepository.delete(id=passenger_id)
        if deleted_rows == 0:
            raise PassengerNotFound(passenger_id)
        return {"message": f"Пассажир {passenger_id} успешно удален."}
