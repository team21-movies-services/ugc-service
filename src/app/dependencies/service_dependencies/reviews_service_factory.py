from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import Settings
from dependencies.clients.mongo import get_mongo_client
from dependencies.registrator import add_factory_to_mapper
from dependencies.settings import get_settings
from repositories.reviews import ReviewsMongoRepository
from services.reviews import ReviewsService, ReviewsServiseABC


@add_factory_to_mapper(ReviewsServiseABC)
def create_reviews_service(
        mongo_client: AsyncIOMotorClient = Depends(get_mongo_client),
        settings: Settings = Depends(get_settings)) -> ReviewsService:

    reviews_repository = ReviewsMongoRepository(mongo_client, settings.mongo)

    return ReviewsService(reviews_repository)
