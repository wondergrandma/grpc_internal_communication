from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from typing import List
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class Film(Base):
    __tablename__ = "Film"

    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column()
    MakeYear: Mapped[int] = mapped_column()
    Hour: Mapped[int] = mapped_column()
    Minute: Mapped[int] = mapped_column()
    Categories: Mapped[str] = mapped_column()
    Overview: Mapped[str] = mapped_column()
    Actors: Mapped[str] = mapped_column()
    Director: Mapped[str] = mapped_column()
    Writer: Mapped[str] = mapped_column()
    Rating: Mapped[int] = mapped_column()
    CoverPath: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return f"""Film(Id={self.Id!r}, Name={self.Name!r}, MakeYear={self.MakeYear!r}, Hour={self.Hour!r}, 
                Minute={self.Minute!r}, Categories={self.Categories!r}, Overview={self.Overview!r}, Actors={self.Actors!r}, Director={self.Director!r}, 
                Writer={self.Writer!r}, Rating={self.Rating!r}, CoverPath={self.CoverPath!r})"""



    
