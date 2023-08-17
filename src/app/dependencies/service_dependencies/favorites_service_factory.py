from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import Settings
from dependencies.clients.mongo import get_mongo_client
from dependencies.registrator import add_factory_to_mapper
from dependencies.settings import get_settings
from repositories.favorites import FavoritesMongoRepository
from services.favorites import FavoritesService, FavoritesServiceABC


@add_factory_to_mapper(FavoritesServiceABC)
def create_favorites_service(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    settings: Settings = Depends(get_settings),
) -> FavoritesService:
    favorite_repository = FavoritesMongoRepository(mongo_client, settings.mongo)
    return FavoritesService(favorite_repository)
