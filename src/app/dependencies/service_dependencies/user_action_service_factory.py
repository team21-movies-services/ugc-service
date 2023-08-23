from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import Settings
from dependencies.clients.mongo import get_mongo_client
from dependencies.registrator import add_factory_to_mapper
from dependencies.settings import get_settings
from repositories.user_action import MongoUserActionRepository
from services.user_action import UserActionService, UserActionServiceABC


@add_factory_to_mapper(UserActionServiceABC)
def create_user_action_service(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    settings: Settings = Depends(get_settings),
) -> UserActionService:
    repository = MongoUserActionRepository(mongo_client, settings)
    return UserActionService(repository)
