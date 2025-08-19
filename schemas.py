from datetime import date
from enum import Enum
from pydantic import BaseModel, validator

class GenreURLChoices(Enum):
    ROCK = "rock"
    GRUNGE = "grunge"
    ELECTRONIC = "electronic"
    ALTERNATIVE = "alternative"
    POP = "pop"
    METAL = "metal"
    HIP_HOP = "hip-hop"
    R_B = "r&b"

class GenreChoices(Enum):
    ROCK = "Rock"
    GRUNGE = "Grunge"
    ELECTRONIC = "Electronic"
    ALTERNATIVE = "Alternative"
    POP = "Pop"
    METAL = "Metal"
    HIP_HOP = "Hip-Hop"
    R_B = "R&B"


class Album(BaseModel):
    title: str
    release_date: date

class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []

class BandCreate(BandBase):
    @validator("genre", pre=True)
    def title_case_genre(cls, value):
        return value.title()

class BandWithID(BandBase):
    id: int