from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import UUID4


class FavoritesRepositoryABC(ABC):
    @abstractmethod
    def get_favorites_by_user_id(self, user_id: UUID4) -> list[dict[str, Any]]:
        raise NotImplementedError


class FavoritesMongoRepository(FavoritesRepositoryABC):
    def __init__(self, client: AsyncIOMotorClient):
        self._client = client

    def get_favorites_by_user_id(self, user_id: UUID4) -> list[dict[str, Any]]:
        return [{"movie_id": uuid4(), "created_at": datetime.now()}]
