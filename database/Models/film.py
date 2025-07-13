from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Models.asociations.actor_film import actor_film
from database.Models.asociations.category_film import category_film
from database.Models.base import Base


class Film(Base):
    __tablename__ = "Film"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column()
    MakeYear: Mapped[int] = mapped_column()
    Hour: Mapped[int] = mapped_column()
    Minute: Mapped[int] = mapped_column()
    Categories: Mapped[List["Category"]] = relationship(
        "Category", secondary=category_film, back_populates="Film"
    )
    Overview: Mapped[str] = mapped_column()
    Actors: Mapped[List["Actor"]] = relationship(
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
