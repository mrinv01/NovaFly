from sqlalchemy.orm import relationship, Mapped
from app.database import Base, int_pk

from app.models.flight import Flight


class Route(Base):
    id: Mapped[int_pk]
    departure_airport: Mapped[str]
    departure_city: Mapped[str]
    arrival_airport: Mapped[str]
    arrival_city: Mapped[str]

    #flights: Mapped[list["Flight"]] = relationship("Flight", back_populates="route")

    def __str__(self):
        return (f"{self.__class__.__name__} (id={self.id}, "
                f"departure_airport={self.departure_airport}, "
                f"departure_city{self.departure_city}), "
                f"arrival_airport={self.arrival_airport}, "
                f"arrival_city{self.arrival_city})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "departure_airport": self.departure_airport,
            "departure_city": self.departure_city,
            "arrival_airport": self.arrival_airport,
            "arrival_city": self.arrival_city
        }