import pytest
from pydantic import ValidationError
from src.schemas.films.film_filter import FilmFilter


def test_year_sets_both_range_bounds() -> None:
    film_filter = FilmFilter(year=2006)

    assert film_filter.year_from == 2006
    assert film_filter.year_to == 2006


def test_rejects_invalid_year_range() -> None:
    with pytest.raises(ValidationError, match="year_from must be less than"):
        FilmFilter(year_from=2010, year_to=2000)


def test_rejects_invalid_length_range() -> None:
    with pytest.raises(ValidationError, match="length_from must be less than"):
        FilmFilter(length_from=120, length_to=60)
