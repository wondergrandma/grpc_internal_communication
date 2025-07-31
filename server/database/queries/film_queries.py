from typing import List

from sqlalchemy import select

from server.database.models.actor import Actor
from server.database.models.category import Category
from server.database.models.director import Director
from server.database.models.film import Film
from server.database.queries import Connector, Session


class FilmQuery:
    session: Session = Connector.session

    @staticmethod
    def get_film(name: str) -> Film | None:
        stmt = select(Film).where(Film.Name == name)
        result = FilmQuery.session.scalar(stmt)

        return result

    @staticmethod
    def create_film(
        name: str,
        make_year: int,
        hour: int,
        minute: int,
        categories: List[Category],
        overview: str,
        actors: List[Actor],
        directors: List[Director],
        rating: int,
        cover_path: str,
    ) -> int:
        try:
            new_film = Film(
                Name=name,
                MakeYear=make_year,
                Hour=hour,
                Minute=minute,
                Categories=categories,
                Overview=overview,
                Actors=actors,
                Directors=directors,
                Rating=rating,
                CoverPath=cover_path,
            )
            FilmQuery.session.add(new_film)
            FilmQuery.session.commit()

            return new_film.Id

        except:
            FilmQuery.session.rollback()
            raise
