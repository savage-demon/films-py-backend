from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import settings

POPULAR_SEARCHES_COLLECTION = "popular_searches"

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


async def connect_mongo() -> None:
    global _client, _db

    if not settings.MONGO_URL:
        return

    _client = AsyncIOMotorClient(settings.MONGO_URL)
    _db = _client.get_default_database()

    collection = _db[POPULAR_SEARCHES_COLLECTION]
    await collection.create_index("normalized", unique=True)
    await collection.create_index([("count", -1)])


async def close_mongo() -> None:
    global _client, _db

    if _client is not None:
        _client.close()

    _client = None
    _db = None


def get_mongo_db() -> AsyncIOMotorDatabase | None:
    return _db
