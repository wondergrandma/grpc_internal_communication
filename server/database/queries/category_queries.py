from sqlalchemy import insert, select
from sqlalchemy.engine.row import Row

from server.database.models.category import Category
from server.database.queries import Connector, Session


class CategoryQuery:
    session: Session = Connector.session

    @staticmethod
    def get_category_by_genre(genre: str) -> Category | None:
        stmt = select(Category).where(Category.Genre == genre)
        result = CategoryQuery.session.scalar(stmt)

        return result

    @staticmethod
    def get_category_by_id(id: int) -> Category | None:
        stmt = select(Category).where(Category.Id == id)
        result = CategoryQuery.session.scalar(stmt)

        return result

    @staticmethod
    def create_category(genre: str) -> Row:
        try:
            stmt = insert(Category).values(Genre=genre)
            result = CategoryQuery.session.execute(stmt)
            CategoryQuery.session.commit()

            return result.inserted_primary_key

        except:
            CategoryQuery.session.rollback()
            raise
