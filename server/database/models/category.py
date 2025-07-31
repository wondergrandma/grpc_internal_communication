from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from server.database.models.asociations.category_film import category_film
from server.database.models.base import Base


class Category(Base):
    __tablename__ = "Category"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Genre: Mapped[str] = mapped_column()
    Film: Mapped[List["Film"]] = relationship(  # type: ignore
        "Film", secondary=category_film, back_populates="Categories"
    )

    def __repr__(self):
        return f"Category(Id={self.Id!r}, Genre={self.Genre!r})"
