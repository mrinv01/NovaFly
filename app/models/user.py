from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, relationship, mapped_column
from app.database import Base, str_uniq, int_pk


class User(Base):
    id: Mapped[int_pk]
    surname: Mapped[str]
    name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), default=1, server_default=text("1"))
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="joined")

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="user")

    def __str__(self):
        return (f"{self.__class__.__name__} (id={self.id}, "
                f"surname={self.surname}, name={self.name}, email={self.email}, "
                f"password={self.password}, role={self.role})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "surname": self.surname,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role
        }