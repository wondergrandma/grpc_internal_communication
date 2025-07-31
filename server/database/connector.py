from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


class Connector:
    engine: Engine = create_engine(
        "postgresql+psycopg2://postgres:admin123admin@localhost:5432/lunar", echo=True
    )
    session: Session = Session(engine)
