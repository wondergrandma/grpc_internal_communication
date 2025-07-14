from database.connector import Connector
from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models.actor import Actor
from database.models.category import Category
from sqlalchemy import insert

class Utils:
    conector: Connector = Connector()
    session: Session = Session(conector.engine)

    @staticmethod
    def get_actor(name, surname):
        try: 
            stmt = select(Actor).where(Actor.Name == name, Actor.Surname == surname)
            result = Utils.session.scalar(stmt)

            return result
        
        except Exception as e:
            return e
        
    @staticmethod
    def create_actor(name, surname) -> bool:
        try:
            stmt = insert(Actor).values(Name=name, Surname=surname)
            Utils.session.execute(stmt)
            Utils.session.commit()

            return True

        except Exception as e: 
            Utils.session.rollback()
            return e