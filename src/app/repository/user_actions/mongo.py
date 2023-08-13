from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from repository.user_actions import AbstractUserActionRepository
from schemas.request.user_actions import Action


class MongoUserActionsRepository(AbstractUserActionRepository):
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.db: AsyncIOMotorDatabase = self.client['user_actions']
        self.collection: AsyncIOMotorCollection = self.db.user_actions

    async def insert_action(self, action: Action):
        result = await self.collection.insert_one(action.model_dump(by_alias=True))
        return result.inserted_id
