from server.database.models.base import Base
from typing import List

from server.database.models.asociations.director_film import director_film
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Director(Base):
    __tablename__ = "Director"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column()
    Surname: Mapped[str] = mapped_column()
    Film: Mapped[List["Film"]] = relationship(  # type: ignore
        "Film", secondary=director_film, back_populates="Directors"
    )

    def __repr__(self):
        return f"Director(Id={self.Id!r}, Name={self.Name!r}, Surname={self.Surname!r})"