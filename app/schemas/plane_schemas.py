from pydantic import BaseModel, Field, ConfigDict

class PlaneSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    model: str = Field(..., title="Модель самолета")
    capacity: int = Field(..., title="Количество мест")


class PlaneSchemaAdd(BaseModel):
    model: str = Field(..., title="Модель самолета")
    capacity: int = Field(..., title="Количество мест")