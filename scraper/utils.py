from typing import List

from sqlalchemy import insert, select
from sqlalchemy.engine.row import Row
from sqlalchemy.orm import Session

from database.connector import Connector
from database.models.actor import Actor
from database.models.category import Category
from database.models.film import Film


class Utils:
    conector: Connector = Connector()
    session: Session = Session(conector.engine)

    @staticmethod
    def get_film(name: str) -> Film | None:
        stmt = select(Film).where(Film.Name == name)
        result = Utils.session.scalar(stmt)

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
        director: str,
        writer: str,
        rating: int,
        cover_path: str,
    ) -> Row:
        try:
            new_film = Film(
                Name=name,
                MakeYear=make_year,
                Hour=hour,
                Minute=minute,
                Categories=categories,
                Overview=overview,
                Actors=actors,
                Director=director,
                Writer=writer,
                Rating=rating,
                CoverPath=cover_path,
            )
            Utils.session.add(new_film)
            Utils.session.commit()

            return new_film.Id

        except:
            Utils.session.rollback()

    @staticmethod
    def get_actor_by_name(name: str, surname: str) -> Actor | None:
        stmt = select(Actor).where(Actor.Name == name, Actor.Surname == surname)
        result = Utils.session.scalar(stmt)

        return result

    @staticmethod
    def get_actor_by_id(id: int) -> Actor | None:
        stmt = select(Actor).where(Actor.Id == id)
        result = Utils.session.scalar(stmt)

        return result

    @staticmethod
    def create_actor(name, surname) -> Row:
        try:
            stmt = insert(Actor).values(Name=name, Surname=surname)
            result = Utils.session.execute(stmt)
            Utils.session.commit()

            return result.inserted_primary_key

        except:
            Utils.session.rollback()

    @staticmethod
    def get_category_by_genre(genre: str) -> Category | None:
        stmt = select(Category).where(Category.Genre == genre)
        result = Utils.session.scalar(stmt)

        return result

    @staticmethod
    def get_category_by_id(id: int) -> Category | None:
        stmt = select(Category).where(Category.Id == id)
        result = Utils.session.scalar(stmt)

        return result

    @staticmethod
    def create_category(genre: str) -> Row:
        try:
            stmt = insert(Category).values(Genre=genre)
            result = Utils.session.execute(stmt)
            Utils.session.commit()

            return result.inserted_primary_key

        except:
            Utils.session.rollback()
