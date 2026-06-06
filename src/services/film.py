from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_pagination.ext.sqlalchemy import paginate

from src.models.film import Film
from src.exceptions.film import FilmNotFoundError
from src.query_builders.film_query_builder import FilmQueryBuilder
from src.schemas.films.film_filter import FilmFilter


class FilmService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_films(self, filter: FilmFilter):
        query = FilmQueryBuilder(filter).build()

        return await paginate(self.db, query)

    async def get_film(self, film_id: int) -> Film:
        query = select(Film).where(Film.id == film_id)
        res = await self.db.execute(query)
        film = res.scalar_one_or_none()

        if film is None:
            raise FilmNotFoundError(film_id)

        return film
