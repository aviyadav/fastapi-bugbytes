from datetime import date
from enum import Enum
from pydantic import BaseModel, validator
from sqlmodel import SQLModel, Field, Relationship

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


class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int | None = Field(default=None, foreign_key="band.id")

class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")

class BandBase(SQLModel):
    name: str
    genre: GenreChoices

class BandCreate(BandBase):
    albums: list[AlbumBase] | None = None
    @validator("genre", pre=True)
    def title_case_genre(cls, value):
        return value.title()

class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")