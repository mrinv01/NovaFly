from pydantic import BaseModel, Field
from typing import Optional

class SAirportBase(BaseModel):
    city: str = Field(..., title="Город")
    airport_code: str = Field(..., title="Код аэропорта (например, SVO, JFK)")

class SAirportCreate(SAirportBase):
    pass

class SAirportUpdate(BaseModel):
    city: Optional[str] = Field(None, title="Город")
    airport_code: Optional[str] = Field(None, title="Код аэропорта")

class SAirportOut(SAirportBase):
    id: int
