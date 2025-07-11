from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy import Table
from database.Models.base import Base

actor_film = Table(
    "ActorFilm",
    Base.metadata,
    Column("ActorsId", ForeignKey("Actor.Id"), primary_key=True),
    Column("FilmId", ForeignKey("Film.Id"), primary_key=True),
)