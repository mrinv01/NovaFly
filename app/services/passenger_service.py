from app.repositories.passenger_repository import PassengerDAO
from app.schemas.passenger_schemas import SCreatePassenger, SUpdatePassenger
from app.schemas.request_body_passenger import RBPassenger
from app.exceptions.PassengerExceptions import PassengerExceptions, InformationNotFoundException


class PassengerService:

    @staticmethod
    async def create_passenger(passenger_data: SCreatePassenger):
        return await PassengerDAO.add(**passenger_data.dict())

    @staticmethod
    async def get_all_passengers():
        return await PassengerDAO.find_all()

    @staticmethod
    async def get_passengers_by_filter(request_body: RBPassenger):
        result = await PassengerDAO.find_all(**request_body.to_dict())
        if not result:
            raise InformationNotFoundException
        return result

    @staticmethod
    async def get_passenger_by_id(passenger_id: int):
        result = await PassengerDAO.find_one_or_none_by_id(passenger_id)
        if result is None:
            raise InformationNotFoundException
        return result

    @staticmethod
    async def update_passenger(passenger_id: int, update_data: SUpdatePassenger):
        update_dict = update_data.dict(exclude_none=True)
        updated_rows = await PassengerDAO.update({"id": passenger_id}, **update_dict)
        if updated_rows == 0:
            return {"message": f"Пассажир с id {passenger_id} не найден или не обновился."}
        return {"message": f"Данные пассажира {passenger_id} успешно обновлены."}

    @staticmethod
    async def delete_passenger(passenger_id: int):
        deleted_rows = await PassengerDAO.delete(id=passenger_id)
        if deleted_rows == 0:
            raise PassengerExceptions.PassengerNotFound(passenger_id)
        return {"message": f"Пассажир {passenger_id} успешно удален."}
