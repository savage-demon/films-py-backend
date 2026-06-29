from typing import Literal

from pydantic import BaseModel, Field, model_validator


class FilmFilter(BaseModel):
    keyword: str | None = None
    title: str | None = None
    genre: str | None = None
    ratings: list[str] = Field(default_factory=list)
    features: list[str] = Field(default_factory=list)
    year: int | None = Field(default=None, ge=1800)
    year_from: int | None = Field(default=None, ge=1800)
    year_to: int | None = Field(default=None, ge=1800)
    length_from: int | None = Field(default=None, ge=0)
    length_to: int | None = Field(default=None, ge=0)

    order_by: str | Literal[
        "title",
        "-title",
        "release_year",
        "-release_year",
    ] = "title"

    @model_validator(mode="after")
    def validate_year_range(self) -> "FilmFilter":
        if self.year is not None:
            self.year_from = self.year
            self.year_to = self.year

        if (
            self.year_from is not None
            and self.year_to is not None
            and self.year_from > self.year_to
        ):
            raise ValueError("year_from must be less than or equal to year_to")

        if (
            self.length_from is not None
            and self.length_to is not None
            and self.length_from > self.length_to
        ):
            raise ValueError("length_from must be less than or equal to length_to")

        return self
