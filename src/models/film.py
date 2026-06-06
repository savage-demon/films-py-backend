from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Float
from src.database import Base

class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(String(1024))
    release_date: Mapped[Date] = mapped_column(Date)
    rating: Mapped[float] = mapped_column(Float)
    genre: Mapped[str] = mapped_column(String(255))
