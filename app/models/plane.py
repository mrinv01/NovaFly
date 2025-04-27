from sqlalchemy.orm import relationship, Mapped
from app.database import Base, int_pk


class Plane(Base):
    id: Mapped[int_pk]
    model: Mapped[str]
    capacity: Mapped[int]

    flights: Mapped[list["Flight"]] = relationship("Flight", back_populates="plane")

    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id}, model={self.model}, capacity={self.capacity})"

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {"id": self.id, "model": self.model, "capacity": self.capacity}