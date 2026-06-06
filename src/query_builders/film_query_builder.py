

from sqlalchemy import Select, select
from src.models.film import Film
from src.schemas.films.film_filter import FilmFilter


class FilmQueryBuilder:
    def __init__(self, filter: FilmFilter):
        self.filter = filter

    def build(self) -> Select:
        query = select(Film)

        query = self._apply_filter(query)
        query = self._apply_sort(query)

        return query

    def _apply_filter(self, query: Select) -> Select:
        f = self.filter

        if f.title:
            query = query.where(Film.title.ilike(f"%{f.title}%"))

        if f.genre:
            query = query.where(Film.genre.ilike(f"%{f.genre}%"))

        if f.rating_gte:
            query = query.where(Film.rating >= f.rating_gte)

        if f.rating_lte:
            query = query.where(Film.rating <= f.rating_lte)

        if f.release_date__gte:
            query = query.where(Film.release_date >= f.release_date__gte)

        return query

    def _apply_sort(self, query: Select) -> Select:
        sort_map = {
            "title": Film.title,
            "rating": Film.rating,
            "release_date": Film.release_date,
        }

        f = self.filter.order_by

        if f.startswith("-"):
            return query.order_by(sort_map[f[1:]].desc())

        query = query.order_by(sort_map[f].asc())
        return query
