from datetime import date
from pydantic import BaseModel, ConfigDict

class FilmResponse(BaseModel):
    id: int
    title: str
    description: str
    release_date: date
    rating: float
    genre: str

    # Включаем поддержку ORM (чтобы Pydantic умел читать свойства из моделей SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)
