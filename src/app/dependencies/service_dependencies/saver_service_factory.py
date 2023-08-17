from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import Settings
from dependencies.clients.mongo import get_mongo_client
from dependencies.registrator import add_factory_to_mapper
from dependencies.settings import get_settings
from repositories.saver import MongoUserActionSaverRepository
from services.saver import ActionSaverService, ActionSaverServiceABC


@add_factory_to_mapper(ActionSaverServiceABC)
def create_saver_service(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    settings: Settings = Depends(get_settings),
) -> ActionSaverService:
    repository = MongoUserActionSaverRepository(mongo_client, settings.mongo)
    return ActionSaverService(repository)
