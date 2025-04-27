from sqlalchemy.orm import Mapped, relationship
from app.database import Base, str_uniq, int_pk


class Role(Base):
    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
