from fastapi import FastAPI, HTTPException, Path, Query
from data import BANDS
from schemas import GenreURLChoices, BandBase, BandCreate, BandWithID
from typing import Annotated

app = FastAPI()


@app.get("/")
async def index() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/about")
async def about() -> str:
    return "This is a sample FastAPI application."


# @app.get("/bands")
# async def bands(genre: GenreURLChoices | None = None, has_albums: bool = False) -> list[BandWithID]:
#     band_list = [BandWithID(**band) for band in BANDS]

#     if genre:
#         band_list = [band for band in band_list if band.genre.value.lower() == genre.value]

#     if has_albums:
#         band_list = [band for band in band_list if len(band.albums) > 0]

#     return band_list

@app.get("/bands")
async def bands(genre: GenreURLChoices | None = None, 
                q: Annotated[str | None, Query(max_length = 10)] = None,
            ) -> list[BandWithID]:
    band_list = [BandWithID(**band) for band in BANDS]

    if genre:
        band_list = [band for band in band_list if band.genre.value.lower() == genre.value]

    if q:
        band_list = [band for band in band_list if q.lower() in band.name.lower()]

    return band_list


@app.get("/bands/{band_id}")
async def bands(band_id: Annotated[int, Path(title="The Band ID")]) -> BandWithID:
    band = next((band for band in BANDS if band["id"] == band_id), None)
    if band is None:
        raise HTTPException(status_code=404, detail="Band not found")
    # return BandWithID(**band)
    return band

@app.get("/bands/genre/{genre}")
async def bands_for_genre(genre: GenreURLChoices) -> list[BandWithID]:
    return [BandWithID(**band) for band in BANDS if band["genre"].lower() == genre.value]

@app.post("/bands", response_model=BandWithID)
async def create_band(band_data: BandCreate) -> BandWithID:
    id = BANDS[-1]["id"] + 1 if BANDS else 1
    new_band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(new_band)
    return new_band
