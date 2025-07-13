from .singleton import SingletonMeta
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class Connector(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, "engine"):
            self.engine: Engine = create_engine("postgresql+psycopg2://postgres:admin123admin@localhost:5432/lunar",echo=True)