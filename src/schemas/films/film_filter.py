from datetime import date
from typing import Literal

from pydantic import BaseModel

class FilmFilter(BaseModel):
    title: str | None = None
    genre: str | None = None

    rating_gte: float | None = None

    rating_lte: float | None = None

    release_date__gte: date | None = None

    order_by: Literal[
            "title",
            "-title",
            "genre",
            "-genre",
            "rating",
            "-rating",
            "release_date",
            "-release_date",
    ] = "title"
