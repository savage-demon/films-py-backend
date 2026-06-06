from fastapi import APIRouter

from src.api.v1 import films

main_api_router = APIRouter(prefix="/v1")

main_api_router.include_router(films.films_router, prefix="/films", tags=["Films"])
