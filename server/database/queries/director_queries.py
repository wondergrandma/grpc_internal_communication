from sqlalchemy import insert, select
from sqlalchemy.engine.row import Row

from server.database.models.director import Director
from server.database.queries import Connector, Session


class DirectorQuery:

    session: Session = Connector.session

    @staticmethod
    def get_director_by_name(name: str, surname: str) -> Director | None:
        stmt = select(Director).where(
            Director.Name == name, Director.Surname == surname
        )
        result = DirectorQuery.session.scalar(stmt)

        return result

    @staticmethod
    def get_director_by_id(id: int) -> Director | None:
        stmt = select(Director).where(Director.Id == id)
        result = DirectorQuery.session.scalar(stmt)

        return result

    @staticmethod
    def create_director(name: str, surname: str) -> Row:
        try:
            stmt = insert(Director).values(Name=name, Surname=surname)
            result = DirectorQuery.session.execute(stmt)
            DirectorQuery.session.commit()

            return result.inserted_primary_key

        except:
            DirectorQuery.session.rollback()
            raise
