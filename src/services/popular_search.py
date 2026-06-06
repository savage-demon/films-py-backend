from datetime import UTC, datetime

from src.config import settings
from src.mongo import POPULAR_SEARCHES_COLLECTION, get_mongo_db


class PopularSearchService:
    def __init__(self) -> None:
        self._collection_name = POPULAR_SEARCHES_COLLECTION

    @property
    def _enabled(self) -> bool:
        return get_mongo_db() is not None

    def _collection(self):
        db = get_mongo_db()

        if db is None:
            raise RuntimeError("MongoDB is not connected")

        return db[self._collection_name]

    @staticmethod
    def _normalize_keyword(keyword: str) -> str:
        return " ".join(keyword.strip().lower().split())

    async def record(self, title: str) -> None:
        if not self._enabled:
            return

        display_title = " ".join(title.strip().split())

        if not display_title:
            return

        normalized = self._normalize_keyword(display_title)
        now = datetime.now(UTC)

        await self._collection().update_one(
            {"normalized": normalized},
            {
                "$inc": {"count": 1},
                "$set": {
                    "keyword": display_title,
                    "last_searched_at": now,
                },
                "$setOnInsert": {"normalized": normalized},
            },
            upsert=True,
        )

        await self._trim_store()

    async def record_titles(self, titles: list[str]) -> None:
        for title in titles:
            await self.record(title)

    async def get_top(self, limit: int | None = None) -> list[dict[str, int | str]]:
        if not self._enabled:
            return []

        effective_limit = limit or settings.POPULAR_SEARCHES_DEFAULT_LIMIT
        effective_limit = max(
            1, min(effective_limit, settings.POPULAR_SEARCHES_STORE_LIMIT)
        )

        cursor = (
            self._collection()
            .find({}, {"_id": 0, "keyword": 1, "count": 1})
            .sort("count", -1)
            .limit(effective_limit)
        )

        return await cursor.to_list(length=effective_limit)

    async def _trim_store(self) -> None:
        store_limit = settings.POPULAR_SEARCHES_STORE_LIMIT
        collection = self._collection()

        total = await collection.count_documents({})

        if total <= store_limit:
            return

        cursor = collection.find({}, {"_id": 1}).sort("count", -1).skip(store_limit)
        ids_to_delete = [doc["_id"] async for doc in cursor]

        if ids_to_delete:
            await collection.delete_many({"_id": {"$in": ids_to_delete}})
