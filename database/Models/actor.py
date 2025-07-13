from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Models.asociations.actor_film import actor_film
from database.Models.base import Base
from database.Models.film import Film


class Actor(Base):
    __tablename__ = "Actor"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column()
    Surname: Mapped[str] = mapped_column()
    Film: Mapped[List["Film"]] = relationship(
        "Film", secondary=actor_film, back_populates="Actors"
    )

    def __repr__(self):
        return f"Actor(Id={self.Id!r}, Name={self.Name!r}, Surname={self.Surname!r})"
