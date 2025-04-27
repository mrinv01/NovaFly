from datetime import date, datetime
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict

class TicketSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int = Field(..., title="ИД заказа")
    passenger_id: int = Field(..., title="ИД пассажира")
    flight_id: int = Field(..., title="ИД рейса")
    seat_number: int = Field(..., title="Номер места")
    price: int = Field(..., title="Стоимость билета")

class SAddTicket(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    passenger_id: int = Field(..., title="ИД пассажира")
    flight_id: int = Field(..., title="ИД рейса")
    seat_number: int = Field(..., title="Номер места")
    price: int = Field(..., title="Стоимость билета")

class SUpdateTicket(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    flight_id: Optional[int] = Field(None, title="ИД рейса")
    seat_number: Optional[int] = Field(None, title="Номер места")
    price: Optional[int] = Field(None, title="Стоимость билета")
