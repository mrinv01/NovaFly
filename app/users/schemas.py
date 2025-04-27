from datetime import date, datetime
from typing import Optional
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    surname: str = Field(..., title="Фамилия пользователя")
    name: str = Field(..., title="Имя пользователя")
    email: EmailStr = Field(..., title="Email пользователя")
    password: str = Field(..., title="Пароль пользователя")
    role : str = Field(..., title="Роль пользователя")