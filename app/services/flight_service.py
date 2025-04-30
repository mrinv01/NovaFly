from app.repositories.flight_repository import FlightDAO
from app.repositories.plane_repository import PlaneRepository
from app.repositories.airport_repository import AirportRepository
from app.schemas.request_body_flight import RequestBodyFlight
from app.schemas.flight_schemas import SAddFlight, SUpdateFlight
from app.exceptions.FlightExceptions import InformationNotFoundException, NoFlights


class FlightService:

    @staticmethod
    async def get_all_flights():
        result = await FlightDAO.find_all()
        if not result:
            raise NoFlights
        return result

    @staticmethod
    async def get_flight_by_filter(request_body: RequestBodyFlight):
        result = await FlightDAO.find_all(**request_body.to_dict())
        if not result:
            raise InformationNotFoundException
        return result

    @staticmethod
    async def get_flight_by_id(flight_id: int):
        result = await FlightDAO.find_one_or_none_by_id(flight_id)
        if result is None:
            raise InformationNotFoundException
        return result

    @staticmethod
    async def add_flight(flight: SAddFlight):
        await PlaneRepository.check_plane(flight.plane_id)
        await AirportRepository.check_airport(flight.departure_from)
        await AirportRepository.check_airport(flight.arrival_to)

        check = await FlightDAO.add(**flight.dict())
        if check:
            return {"message": "Рейс успешно создан!", "flight": flight}
        return {"message": "При создании рейса произошла ошибка!"}

    @staticmethod
    async def update_flight(flight_id: int, update_data: SUpdateFlight):
        update_dict = update_data.dict(exclude_none=True)
        updated_rows = await FlightDAO.update_flight_info(flight_id, **update_dict)
        if updated_rows == 0:
            raise InformationNotFoundException
        return {"message": f"Рейс {flight_id} успешно обновлён"}
