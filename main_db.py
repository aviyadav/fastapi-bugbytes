from fastapi import FastAPI, HTTPException, Path, Query, Depends
from models import GenreURLChoices, BandCreate, Band, Album
from contextlib import asynccontextmanager
from db import init_db, engine, get_session
from sqlmodel import Session, select
from typing import Annotated


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    # Here you could close the database connection if needed


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/about")
async def about() -> str:
    return "This is a sample FastAPI application."

@app.post("/bands", response_model=Band)
async def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session)
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album_data in band_data.albums:
            album = Album(
                title=album_data.title, 
                release_date=album_data.release_date, 
                band=band
            )
            session.add(album)
            # band.albums.append(album)

    session.commit()
    session.refresh(band)
    
    return band


@app.get("/bands/{band_id}")
async def bands(
    band_id: Annotated[int, Path(title="The Band ID")],
    session: Session = Depends(get_session)
) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    return band


@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None, 
    q: Annotated[str | None, Query(max_length = 10)] = None,
    session: Session = Depends(get_session)
) -> list[Band]:
    band_list = session.exec(select(Band)).all()

    if genre:
        band_list = [band for band in band_list if band.genre.value.lower() == genre.value]

    if q:
        band_list = [band for band in band_list if q.lower() in band.name.lower()]

    return band_list

@app.get("/bands/genre/{genre}")
async def bands_for_genre(genre: GenreURLChoices, session: Session = Depends(get_session)) -> list[Band]:

    band_list = session.exec(select(Band).filter(Band.genre == genre.value)).all()
    
    # band_list = session.exec(select(Band))
    # band_list = [band for band in band_list if band.genre.value.lower() == genre.value]
    return band_list