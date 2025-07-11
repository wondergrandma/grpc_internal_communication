from sqlalchemy import Column, ForeignKey, Table

from database.Models.base import Base

category_film = Table(
    "CategoryFilm",
    Base.metadata,
    Column("CategoriesId", ForeignKey("Category.Id"), primary_key=True),
    Column("FilmId", ForeignKey("Film.Id"), primary_key=True),
)
