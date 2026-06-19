from src.exceptions.base import EntityNotFoundError


class FilmNotFoundError(EntityNotFoundError):
    def __init__(self, film_id: int):
        self.message = f"Film with id {film_id} not found"
        super().__init__(self.message)
