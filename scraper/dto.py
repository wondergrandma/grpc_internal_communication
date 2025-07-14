from pydantic import BaseModel
from typing import List

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