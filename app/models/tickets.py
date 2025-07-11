from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, int_pk

class Ticket(Base):
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    passenger_id: Mapped[int] = mapped_column(ForeignKey('passengers.id'), nullable=False)
    flight_id: Mapped[int] = mapped_column(ForeignKey('flights.id'), nullable=False)
    seat_number: Mapped[str]
    price: Mapped[int]

    user: Mapped["User"] = relationship("User", back_populates="tickets")
    passenger: Mapped["Passenger"] = relationship("Passenger", back_populates="tickets")
    flight: Mapped["Flight"] = relationship("Flight", back_populates="tickets")

    def __str__(self):
        return (f"{self.__class__.__name__} (id={self.id}, "
                f"user_id={self.order_id}, passenger_id={self.passenger_id}, "
                f"flight_id={self.flight_id}, seat_number={self.seat_number}, "
                f"price={self.price})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "passenger_id": self.passenger_id,
            "flight_id": self.flight_id,
            "seat_number": self.seat_number,
            "price": self.price
        }