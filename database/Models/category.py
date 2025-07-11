from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.Models.asociations.category_film import category_film
from database.Models.base import Base


class Category(Base):
    __tablename__ = "Category"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Genre: Mapped[str] = mapped_column()
    Film: Mapped[List["Film"]] = relationship(
        "Film", secondary=category_film, back_populates="Categories"
    )

    def __repr__(self):
        return f"Category(Id={self.Id!r}, Genre={self.Genre!r})"
