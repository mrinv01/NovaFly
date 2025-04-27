from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, int_pk


class Airport(Base):
    id: Mapped[int_pk]
    city: Mapped[str]
    airport_code: Mapped[str]

    departing_flights = relationship("Flight", foreign_keys="Flight.departure_from", back_populates="departure_airport")
    arriving_flights = relationship("Flight", foreign_keys="Flight.arrival_to", back_populates="arrival_airport")