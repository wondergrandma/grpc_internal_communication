from typing import List

from pydantic import BaseModel


class ScrapedFilm(BaseModel):
    Name: str
    MakeYear: int
    Hour: int
    Minute: int
    Categories: List
    Overview: str
    Actors: List
    Director: str
    Writer: str
    Rating: int
    CoverPath: str
