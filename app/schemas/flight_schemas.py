from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class FlightSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    plane_id: int = Field(..., title="ID модели самолета")
    departure_from: int = Field(..., title="ID места вылета")
    arrival_to: int = Field(..., title="ID места прилета")
    departure: datetime = Field(..., title="Дата и время вылета в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
    arrival: datetime = Field(..., title="Дата и время прилета вв формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
    status: str = Field(..., title="Статус рейса (Например: Готов, Отменен")


class SAddFlight(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    plane_id: int = Field(..., title="ID модели самолета")
    departure_from: int = Field(..., title="ID места вылета")
    arrival_to: int = Field(..., title="ID места прилета")
    departure: datetime = Field(..., title="Дата и время вылета в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
    arrival: datetime = Field(..., title="Дата и время прилета вв формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
    status: str = Field(..., title="Статус рейса (Например: Готов, Отменен")


class SUpdateFlight(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    plane_id: Optional[int] = Field(None, title="ID модели самолета")
    departure_from: Optional[int] = Field(None, title="ID места вылета")
    arrival_to: Optional[int] = Field(None, title="ID места прилета")
    departure: Optional[datetime] = Field(None, title="Дата и время вылета в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
    arrival: Optional[datetime] = Field(None, title="Дата и время прилета в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
    status: Optional[str] = Field(None, title="Статус рейса (Например: Готов, Отменен)")
