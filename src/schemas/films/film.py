from pydantic import BaseModel, ConfigDict


class FilmResponse(BaseModel):
    id: int
    title: str
    description: str | None
    release_year: int | None
    rental_duration: int
    rental_rate: float
    length: int | None
    replacement_cost: float
    rating: str | None
    genres: list[str]
    features: list[str]

    # Включаем поддержку ORM (чтобы Pydantic умел читать свойства из моделей SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)


class FilmListResponse(BaseModel):
    items: list[FilmResponse]
    total: int
    page: int
    size: int
    pages: int


class FilmSearchMetaResponse(BaseModel):
    genres: list[str]
    ratings: list[str]
    features: list[str]
    min_release_year: int | None
    max_release_year: int | None
    min_length: int | None
    max_length: int | None
