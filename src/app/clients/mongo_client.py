from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import MongoConfig


class AsyncMongoClient:
    def __init__(self, mongo_client: AsyncIOMotorClient, mongo_config: MongoConfig):
        self._mongo_client = mongo_client
        self._collection = self._mongo_client[mongo_config.database][mongo_config.collection]

    def collection_find(self, action_type: str, film_id: UUID | None = None, user_id: UUID | None = None):
        stmt = {"action_type": action_type}
        if film_id:
            stmt["film_id"] = str(film_id)
        cursor = self._collection.find(stmt)
        return cursor
