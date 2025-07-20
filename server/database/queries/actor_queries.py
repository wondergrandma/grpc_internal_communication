from sqlalchemy import insert, select
from sqlalchemy.engine.row import Row

from server.database.models.actor import Actor
from server.database.queries import Connector, Session


class ActorQuery:

    session: Session = Connector.session

    @staticmethod
    def get_actor_by_name(name: str, surname: str) -> Actor | None:
        stmt = select(Actor).where(Actor.Name == name, Actor.Surname == surname)
        result = ActorQuery.session.scalar(stmt)

        return result

    @staticmethod
    def get_actor_by_id(id: int) -> Actor | None:
        stmt = select(Actor).where(Actor.Id == id)
        result = ActorQuery.session.scalar(stmt)

        return result

    @staticmethod
    def create_actor(name, surname) -> Row:
        try:
            stmt = insert(Actor).values(Name=name, Surname=surname)
            result = ActorQuery.session.execute(stmt)
            ActorQuery.session.commit()

            return result.inserted_primary_key

        except:
            ActorQuery.session.rollback()
            raise
