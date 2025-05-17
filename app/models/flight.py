from sqlalchemy import ForeignKey, Date, Time
from datetime import date, time
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, int_pk


class Flight(Base):
    id: Mapped[int_pk]
    plane_id: Mapped[int] = mapped_column(ForeignKey('planes.id'), nullable=False)
    departure_from: Mapped[int] = mapped_column(ForeignKey('airports.id'), nullable=False)
    arrival_to: Mapped[int] = mapped_column(ForeignKey('airports.id'), nullable=False)
    departure_date: Mapped[date] = mapped_column(Date, nullable=False)
    departure_time: Mapped[time] = mapped_column(Time, nullable=False)
    arrival_date: Mapped[date] = mapped_column(Date, nullable=False)
    arrival_time: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[str]

    plane: Mapped["Plane"] = relationship("Plane", back_populates="flights")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="flight")
    departure_airport = relationship("Airport", foreign_keys=[departure_from], back_populates="departing_flights")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_to], back_populates="arriving_flights")

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
