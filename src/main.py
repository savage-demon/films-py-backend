from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import main_api_router
from src.config import settings
from src.exceptions.handler import register_exception_handlers
from src.mongo import close_mongo, connect_mongo


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await connect_mongo()

    yield

    await close_mongo()


app = FastAPI(title=settings.APP_TITLE, version=settings.APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(main_api_router)

register_exception_handlers(app)
