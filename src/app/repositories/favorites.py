from abc import ABC, abstractmethod
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import MongoConfig
from schemas.request.user_actions import ActionType
from schemas.response.favorites import FavoriteMovie


class FavoritesRepositoryABC(ABC):
    @abstractmethod
    async def get_favorites_by_user_id(self, user_id: UUID) -> list[FavoriteMovie]:
        raise NotImplementedError


class FavoritesMongoRepository(FavoritesRepositoryABC):
    def __init__(self, client: AsyncIOMotorClient, config: MongoConfig):
        self._client = client
        self._db = config.database
        self._collection = config.collection

    async def get_favorites_by_user_id(self, user_id: UUID) -> list[FavoriteMovie]:
        collection = self._client[self._db][self._collection]
        favorites_cursor = collection.find({"user_id": str(user_id), "action_type": ActionType.favorite})
        return [FavoriteMovie.map_from_mongo(favorite) async for favorite in favorites_cursor]
