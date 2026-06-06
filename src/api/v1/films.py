from fastapi import APIRouter, Depends 
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.schemas.films.film import FilmResponse
from src.schemas.films.film_filter import FilmFilter
from src.services.film import FilmService

films_router = APIRouter()

def get_film_service(db: AsyncSession = Depends(get_async_session)) -> FilmService:
    return FilmService(db)


@films_router.get("/", response_model=Page[FilmResponse])
async def get_films(
    service: FilmService = Depends(get_film_service),
    filter: FilmFilter = Depends(),
):
    return await service.get_films(filter)



@films_router.get("/{film_id}", response_model=FilmResponse)
async def get_film(
    film_id: int,
    service: FilmService = Depends(get_film_service)
):
    return await service.get_film(film_id)
