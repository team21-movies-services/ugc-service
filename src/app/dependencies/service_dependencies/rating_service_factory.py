from fastapi import Depends

from clients.mongo_client import AsyncMongoClient
from dependencies.clients.mongo import get_async_mongo_client
from dependencies.registrator import add_factory_to_mapper
from repositories.rating import RatingMongoRepository
from services.rating import RatingService, RatingServiceABC


@add_factory_to_mapper(RatingServiceABC)
def create_rating_service(
    async_mongo_client: AsyncMongoClient = Depends(get_async_mongo_client),
) -> RatingService:
    return RatingService(rating_repository=RatingMongoRepository(async_mongo_client))
