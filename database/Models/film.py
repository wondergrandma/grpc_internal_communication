from typing import List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.asociations.actor_film import actor_film
from database.models.asociations.category_film import category_film
from database.models.base import Base


class Film(Base):
    __tablename__ = "Film"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column()
    MakeYear: Mapped[int] = mapped_column()
    Hour: Mapped[int] = mapped_column()
    Minute: Mapped[int] = mapped_column()
    Categories: Mapped[List["Category"]] = relationship(  # type: ignore
        "Category", secondary=category_film, back_populates="Film"
    )
    Overview: Mapped[str] = mapped_column()
    Actors: Mapped[List["Actor"]] = relationship(  # type: ignore
        "Actor", secondary=actor_film, back_populates="Film"
    )
    Director: Mapped[str] = mapped_column()
    Writer: Mapped[str] = mapped_column()
    Rating: Mapped[int] = mapped_column()
    CoverPath: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"""Film(Id={self.Id!r}, Name={self.Name!r}, MakeYear={self.MakeYear!r}, Hour={self.Hour!r}, 
                Minute={self.Minute!r}, Categories={self.Categories!r}, Overview={self.Overview!r}, Actors={self.Actors!r}, Director={self.Director!r}, 
                Writer={self.Writer!r}, Rating={self.Rating!r}, CoverPath={self.CoverPath!r})"""
