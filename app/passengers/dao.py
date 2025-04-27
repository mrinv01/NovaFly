from app.dao.base import BaseDAO
from app.models.passenger import Passenger

class PassengerDAO(BaseDAO):
    model = Passenger
