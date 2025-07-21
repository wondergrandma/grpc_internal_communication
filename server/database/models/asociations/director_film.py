from sqlalchemy import Column, ForeignKey, Table

from server.database.models.base import Base

director_film = Table(
    "DirectorFilm",
    Base.metadata,
    Column("DirectorsId", ForeignKey("Director.Id"), primary_key=True),
    Column("FilmId", ForeignKey("Film.Id"), primary_key=True)
)