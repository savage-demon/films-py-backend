from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.schemas.films.film import (
    FilmListResponse,
    FilmResponse,
    FilmSearchMetaResponse,
)
from src.schemas.films.film_filter import FilmFilter
from src.schemas.films.popular_search import PopularSearchListResponse
from src.services.film import FilmService
from src.services.popular_search import PopularSearchService

films_router = APIRouter()


def get_film_service(
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> FilmService:
    return FilmService(db)


def get_popular_search_service() -> PopularSearchService:
    return PopularSearchService()


def get_film_filter(
    keyword: str | None = None,
    title: str | None = None,
    genre: str | None = None,
    ratings: Annotated[list[str] | None, Query()] = None,
    features: Annotated[list[str] | None, Query()] = None,
    year: Annotated[int | None, Query(ge=1800)] = None,
    year_from: Annotated[int | None, Query(ge=1800)] = None,
    year_to: Annotated[int | None, Query(ge=1800)] = None,
    length_from: Annotated[int | None, Query(ge=0)] = None,
    length_to: Annotated[int | None, Query(ge=0)] = None,
    order_by: str = "title",
) -> FilmFilter:
    return FilmFilter(
        keyword=keyword,
        title=title,
        genre=genre,
        ratings=ratings or [],
        features=features or [],
        year=year,
        year_from=year_from,
        year_to=year_to,
        length_from=length_from,
        length_to=length_to,
        order_by=order_by,
    )


@films_router.get("/search-meta", response_model=FilmSearchMetaResponse)
async def get_search_meta(
    service: Annotated[FilmService, Depends(get_film_service)],
):
    return await service.get_search_meta()


@films_router.get("/popular-searches", response_model=PopularSearchListResponse)
async def get_popular_searches(
    popular_search_service: Annotated[
        PopularSearchService, Depends(get_popular_search_service)
    ],
    limit: Annotated[int, Query(ge=1, le=20)] = 5,
):
    items = await popular_search_service.get_top(limit=limit)

    return {"items": items}


@films_router.get("/", response_model=FilmListResponse)
async def get_films(
    service: Annotated[FilmService, Depends(get_film_service)],
    popular_search_service: Annotated[
        PopularSearchService, Depends(get_popular_search_service)
    ],
    filter: Annotated[FilmFilter, Depends(get_film_filter)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    result = await service.get_films(filter, page=page, size=size)

    search_query = (filter.keyword or filter.title or "").strip()

    if search_query and page == 1 and result["total"] > 0:
        found_titles = [film.title for film in result["items"] if film.title]
        await popular_search_service.record_titles(found_titles)

    return result


@films_router.get("/{film_id}", response_model=FilmResponse)
async def get_film(
    film_id: int,
    service: Annotated[FilmService, Depends(get_film_service)],
):
    return await service.get_film(film_id)
