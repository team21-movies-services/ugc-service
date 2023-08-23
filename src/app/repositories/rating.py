from abc import ABC, abstractmethod
from typing import AsyncGenerator
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import MongoConfig
from schemas.request.user_actions import ActionType


class RatingRepositoryABC(ABC):
    @abstractmethod
    async def get_film_rates(self, film_id: UUID):
        """Получение списка оценок фильма"""
        raise NotImplementedError


class RatingMongoRepository(RatingRepositoryABC):
    def __init__(self, client: AsyncIOMotorClient, config: MongoConfig):
        self._client = client
        self._collection = self._client[config.database][config.collection]

    async def get_film_rates(self, film_id: UUID) -> AsyncGenerator[int, None]:
        rows = self._collection.find({"action_type": ActionType.rating, "film_id": str(film_id)})
        return (row.get('action_data', {}).get('rate', 0) async for row in rows)
