from sqlalchemy import ForeignKey, func, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, int_pk
from datetime import datetime

class Order(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[str] = mapped_column(default= "Создан")

    #user: Mapped["User"] = relationship("User", back_populates="orders")
    #tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="order")

    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id}, user_id={self.user_id}, created_at={self.created_at})"

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at
        }