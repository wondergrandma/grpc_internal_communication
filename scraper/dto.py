from pydantic import BaseModel
from typing import Union

class ScrapedFilm(BaseModel):
    title: str
    make_year: int
    age_restriction: Union[int, str]
    length: int
    overview: str

    class Config:
        allow_mutation = False
