from fastapi import FastAPI, HTTPException
from data import BANDS
from schemas import GenreURLChoices, Band

app = FastAPI()


@app.get("/")
async def index() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/about")
async def about() -> str:
    return "This is a sample FastAPI application."


@app.get("/bands")
async def bands(genre: GenreURLChoices | None = None, has_albums: bool = False) -> list[Band]:
    band_list = [Band(**band) for band in BANDS]

    if genre:
        band_list = [band for band in band_list if band.genre.lower() == genre.value]
    
    if has_albums:
        band_list = [band for band in band_list if len(band.albums) > 0]

    return band_list


@app.get("/bands/{band_id}")
async def bands(band_id: int) -> Band:
    band = next((band for band in BANDS if band["id"] == band_id), None)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    return Band(**band)

@app.get("/bands/genre/{genre}")
async def bands_for_genre(genre: GenreURLChoices) -> list[Band]:
    return [Band(**band) for band in BANDS if band["genre"].lower() == genre.value]
