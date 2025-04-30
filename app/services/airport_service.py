from app.schemas.airport_schemas import SAirportCreate, SAirportUpdate
from app.repositories.airport_repository import AirportRepository
from app.exceptions.AirportExceptions import AirportExceptions, InformationNotFoundException

class AirportService:

    @staticmethod
    async def create_airport(data: SAirportCreate):
        return await AirportRepository.add(**data.dict())

    @staticmethod
    async def get_all_airports():
        return await AirportRepository.find_all()

    @staticmethod
    async def get_airport_by_id(airport_id: int):
        airport = await AirportRepository.find_one_or_none_by_id(airport_id)
        if not airport:
            raise AirportExceptions.AirportNotFound(airport_id)
        return airport

    @staticmethod
    async def search_by_city(city: str):
        airports = await AirportRepository.find_by_city(city)
        if not airports:
            raise InformationNotFoundException
        return airports

    @staticmethod
    async def update_airport(airport_id: int, data: SAirportUpdate):
        update_data = data.dict(exclude_none=True)
        updated = await AirportRepository.update({"id": airport_id}, **update_data)
        if updated == 0:
            raise AirportExceptions.AirportNotFound(airport_id)
        return await AirportRepository.find_one_or_none_by_id(airport_id)

    @staticmethod
    async def delete_airport(airport_id: int):
        deleted = await AirportRepository.delete(id=airport_id)
        if deleted == 0:
            raise AirportExceptions.AirportNotFound(airport_id)
        return {"message": f"Аэропорт с id {airport_id} успешно удалён"}
