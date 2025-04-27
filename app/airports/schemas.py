from pydantic import BaseModel, Field, ConfigDict

class SAirport(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    city: str = Field(..., title="Город")
    airport_code: str = Field(..., title="Код ИАТА аэропорта (Например: KRR-код аэропорта Краснодара")

class SAddAirport(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    city: str = Field(..., title="Город")
    airport_code: str = Field(..., title="Код ИАТА аэропорта (Например: KRR-код аэропорта Краснодара")

