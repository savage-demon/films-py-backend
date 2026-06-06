from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import main_api_router
from src.config import settings
from fastapi_pagination import add_pagination
from src.exceptions.handler import register_exception_handlers


app = FastAPI(title=settings.APP_TITLE, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(main_api_router)

add_pagination(app)

register_exception_handlers(app)
