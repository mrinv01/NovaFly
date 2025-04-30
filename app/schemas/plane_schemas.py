from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class PlaneSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    model: str = Field(..., title="Модель самолета")
    capacity: int = Field(..., title="Количество мест")


class PlaneSchemaAdd(BaseModel):
    model: str = Field(..., title="Модель самолета")
    capacity: int = Field(..., title="Количество мест")

class PlaneSchemaUpdate(BaseModel):
    model: Optional[str] = Field(None, title="Модель самолета")
    capacity: Optional[int] = Field(None, title="Количество мест")