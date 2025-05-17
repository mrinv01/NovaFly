from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class FlightSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    plane_id: int = Field(..., title="ID модели самолета")
    departure_from: int = Field(..., title="ID места вылета")
    arrival_to: int = Field(..., title="ID места прилета")
    departure_date: date = Field(..., title="Дата вылета в формате ГГГГ-ММ-ДД")
    departure_time: time = Field(..., title="Время вылета в формате ЧЧ:ММ:СС")
    arrival_date: date = Field(..., title="Дата прилета вв формате ГГГГ-ММ-ДД")
    arrival_time: time = Field(..., title="Время прилета в формате ЧЧ:ММ:СС")
    status: str = Field(..., title="Статус рейса (Например: Готов, Отменен")


class SAddFlight(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    plane_id: int = Field(..., title="ID модели самолета")
    departure_from: int = Field(..., title="ID места вылета")
    arrival_to: int = Field(..., title="ID места прилета")
    departure_date: date = Field(..., title="Дата вылета в формате ГГГГ-ММ-ДД")
    departure_time: time = Field(..., title="Время вылета в формате ЧЧ:ММ:СС")
    arrival_date: date = Field(..., title="Дата прилета вв формате ГГГГ-ММ-ДД")
    arrival_time: time = Field(..., title="Время прилета в формате ЧЧ:ММ:СС")
    status: str = Field(..., title="Статус рейса (Например: Готов, Отменен")


class SUpdateFlight(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    plane_id: Optional[int] = Field(None, title="ID модели самолета")
    departure_from: Optional[int] = Field(None, title="ID места вылета")
    arrival_to: Optional[int] = Field(None, title="ID места прилета")
    departure_date: date = Field(..., title="Дата вылета в формате ГГГГ-ММ-ДД")
    departure_time: time = Field(..., title="Время вылета в формате ЧЧ:ММ:СС")
    arrival_date: date = Field(..., title="Дата прилета вв формате ГГГГ-ММ-ДД")
    arrival_time: time = Field(..., title="Время прилета в формате ЧЧ:ММ:СС")
    status: Optional[str] = Field(None, title="Статус рейса (Например: Готов, Отменен)")
