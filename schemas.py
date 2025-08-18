from datetime import date
from enum import Enum
from pydantic import BaseModel

class GenreURLChoices(Enum):
    ROCK = "rock"
    GRUNGE = "grunge"
    ELECTRONIC = "electronic"
    ALTERNATIVE = "alternative"
    POP = "pop"
    METAL = "metal"
    HIP_HOP = "hip-hop"
    R_B = "r&b"


class Album(BaseModel):
    title: str
    release_date: date

class Band(BaseModel):
    id: int
    name: str
    genre: str
    albums: list[Album] = []
