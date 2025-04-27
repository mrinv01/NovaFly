from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, int_pk


class Flight(Base):
    id: Mapped[int_pk]
    plane_id: Mapped[int] = mapped_column(ForeignKey('planes.id'), nullable=False)
    departure_from: Mapped[int] = mapped_column(ForeignKey('airports.id'), nullable=False)
    arrival_to: Mapped[int] = mapped_column(ForeignKey('airports.id'), nullable=False)
    departure: Mapped[datetime]
    arrival: Mapped[datetime]
    status: Mapped[str]

    plane: Mapped["Plane"] = relationship("Plane", back_populates="flights")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="flight")
    departure_airport = relationship("Airport", foreign_keys=[departure_from], back_populates="departing_flights")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_to], back_populates="arriving_flights")

    @property
    def departure_date(self):
        return self.departure.date()

    @property
    def departure_time(self):
        return self.departure.time()

    @property
    def arrival_date(self):
        return self.arrival.date()

    @property
    def arrival_time(self):
        return self.arrival.time()

    def __str__(self):
        return (f"Рейс #{self.id} | "
                f"{self.departure_date} {self.departure_time.strftime('%H:%M')} → "
                f"{self.arrival_date} {self.arrival_time.strftime('%H:%M')} | "
                f"Статус: {self.status}")


    def __repr__(self):
        return (f"<Flight(id={self.id}, "
                f"plane_id={self.plane_id}, "
                f"route_id={self.route_id}, "
                f"departure='{self.departure_date} {self.departure_time.strftime('%H:%M')}', "
                f"arrival='{self.arrival_date} {self.arrival_time.strftime('%H:%M')}', "
                f"status='{self.status}')>")

    def to_dict(self):
        return {
            "id": self.id,
            "plane_id": self.plane_id,
            "route_id": self.route_id,
            "departure_date": self.departure_date,
            "departure_time": self.departure_time,
            "arrival_date": self.arrival_date,
            "arrival_time": self.arrival_time,
            "status": self.status
        }
