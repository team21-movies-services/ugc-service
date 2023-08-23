from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import Settings
from dependencies.clients.mongo import get_mongo_client
from dependencies.registrator import add_factory_to_mapper
from dependencies.settings import get_settings
from repositories.rating import RatingMongoRepository
from services.rating import RatingService, RatingServiceABC


@add_factory_to_mapper(RatingServiceABC)
def create_rating_service(
    mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
    settings: Settings = Depends(get_settings),
) -> RatingService:
    rating_repository = RatingMongoRepository(mongo_client, settings.mongo)
    return RatingService(rating_repository)
