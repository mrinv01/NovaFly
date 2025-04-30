from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class OrderSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    status: str = Field(..., title="Статус заказа")

class SAddOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int = Field(..., title="ID пользователя, создавшего заказ")

class SUpdateOrder(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    status: str = Field(..., title="Статус заказа")