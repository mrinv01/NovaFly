from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional

class SCreatePassenger(BaseModel):
    surname: str = Field(..., title="Фамилия")
    name: str = Field(..., title="Имя")
    patronymic: Optional[str] = Field(None, title="Отчество")
    date_of_birth: date = Field(..., title="Дата рождения")
    document_number: int = Field(..., title="Номер документа")

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value

class SUpdatePassenger(BaseModel):
    surname: Optional[str] = Field(None, title="Фамилия")
    name: Optional[str] = Field(None, title="Имя")
    patronymic: Optional[str] = Field(None, title="Отчество")
    date_of_birth: Optional[date] = Field(None, title="Дата рождения")
    document_number: Optional[int] = Field(None, title="Номер документа")

    @field_validator("date_of_birth")
    def validate_date_of_birth(cls, value):
        if value and value >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return value

class SPassengerOut(SCreatePassenger):
    id: int

