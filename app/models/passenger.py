from sqlalchemy.orm import Mapped, relationship
from app.database import Base, int_pk, str_not_null, str_null_true
from datetime import date

class Passenger(Base):
    id: Mapped[int_pk]
    surname: Mapped[str_not_null]
    name: Mapped[str_not_null]
    patronymic: Mapped[str_null_true]
    date_of_birth: Mapped[date]
    document_number: Mapped[int]

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="passenger")

    def __str__(self):
        return (f"{self.__class__.__name__} (id={self.id}, "
                f"surname={self.surname}, name={self.name}, "
                f"patronymic={self.patronymic}, "
                f"date_of_birth={self.date_of_birth}, "
                f"document_number={self.document_number})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "surname": self.surname,
            "name": self.name,
            "patronymic": self.patronymic,
            "date_of_birth": self.date_of_birth,
            "document_number": self.document_number
        }