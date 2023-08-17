from abc import ABC, abstractmethod

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from core.config import MongoConfig
from schemas.request.user_actions import Action


class ActionSaverRepositoryABC(ABC):
    @abstractmethod
    async def insert_action(self, action: Action):
        """Метод для сохранения действий пользователя в mongodb"""
        pass


class MongoUserActionSaverRepository(ActionSaverRepositoryABC):
    def __init__(self, client: AsyncIOMotorClient, settings: MongoConfig):
        self.client = client
        self.db: AsyncIOMotorDatabase = self.client[settings.database]
        self.collection: AsyncIOMotorCollection = self.db[settings.collection]

    async def insert_action(self, action: Action):
        result = await self.collection.insert_one(action.model_dump(by_alias=True, exclude_none=True))
        return result
