from abc import ABC, abstractmethod
from typing import AsyncGenerator
from uuid import UUID

from clients.mongo_client import AsyncMongoClient
from schemas.request.user_actions import ActionType


class RatingRepositoryABC(ABC):
    @abstractmethod
    async def get_film_rates(self, film_id: UUID):
        """Получение списка оценок фильма"""
        raise NotImplementedError


class RatingMongoRepository(RatingRepositoryABC):
    def __init__(self, async_mongo_client: AsyncMongoClient) -> None:
        self._async_mongo_client = async_mongo_client

    async def get_film_rates(self, film_id: UUID) -> AsyncGenerator[int, None]:
        rows = self._async_mongo_client.collection_find(action_type=ActionType.rating, film_id=film_id)
        return (row.get('action_data', {}).get('rate', 0) async for row in rows)
