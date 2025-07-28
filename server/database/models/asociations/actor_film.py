from sqlalchemy import Column, ForeignKey, Table

from server.database.models.base import Base

actor_film = Table(
    "ActorFilm",
    Base.metadata,
    Column("ActorsId", ForeignKey("Actor.Id"), primary_key=True, nullable=True),
    Column("FilmId", ForeignKey("Film.Id"), primary_key=True, nullable=True),
)
