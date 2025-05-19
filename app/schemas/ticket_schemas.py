from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class TicketSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int = Field(..., title="ИД пользователя")
    passenger_id: int = Field(..., title="ИД пассажира")
    flight_id: int = Field(..., title="ИД рейса")
    seat_number: str = Field(..., title="Номер места")
    price: int = Field(..., title="Стоимость билета")

class SAddTicket(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    passenger_id: int = Field(..., title="ИД пассажира")
    flight_id: int = Field(..., title="ИД рейса")
    seat_number: str = Field(..., title="Номер места")
    price: int = Field(..., title="Стоимость билета")

class SUpdateTicket(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    flight_id: Optional[int] = Field(None, title="ИД рейса")
    seat_number: Optional[str] = Field(None, title="Номер места")
    price: Optional[int] = Field(None, title="Стоимость билета")
