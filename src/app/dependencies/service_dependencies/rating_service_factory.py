from fastapi import Depends

from dependencies.registrator import add_factory_to_mapper

from repositories.rating import RatingMongoRepository
from services.rating import RatingServiceABC, RatingService

from clients.mongo_client import AsyncMongoClient
from dependencies.clients.mongo import get_async_mongo_client


@add_factory_to_mapper(RatingServiceABC)
def create_rating_service(
    async_mongo_client: AsyncMongoClient = Depends(get_async_mongo_client),
) -> RatingService:
    return RatingService(rating_repository=RatingMongoRepository(async_mongo_client))
