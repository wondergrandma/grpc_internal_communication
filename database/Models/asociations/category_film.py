from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Table
from database.Models.base import Base

category_film = Table(
    "CategoryFilm",
    Base.metadata,
    Column("CategoriesId", ForeignKey("Category.Id"), primary_key=True),
    Column("FilmId", ForeignKey("Film.Id"), primary_key=True),
)