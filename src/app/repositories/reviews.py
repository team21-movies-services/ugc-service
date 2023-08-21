from abc import ABC, abstractmethod
from collections import defaultdict
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import MongoConfig
from schemas.request.user_actions import ActionType
from schemas.response.reviews import FilmReview


class ReviewsRepositoryABC(ABC):
    @abstractmethod
    async def get_all_reviews_by_film_id(self, film_id: UUID) -> list[FilmReview]:
        raise NotImplementedError

    @abstractmethod
    async def _get_users_film_rating(self, user_id: UUID, film_id: UUID) -> int | None:
        """Получение оценки конкретного фильма конкретным юзером"""
        raise NotImplementedError

    @abstractmethod
    async def _get_review_rating(self, review_id: str) -> dict[str, int]:
        """Получение рейтинга рецензии на основе лайков/дизлайков"""
        raise NotImplementedError

    @abstractmethod
    async def get_all_reviews_by_user_id(self, user_id: UUID) -> list[FilmReview]:
        raise NotImplementedError


class ReviewsMongoRepository(ReviewsRepositoryABC):
    def __init__(self, client: AsyncIOMotorClient, config: MongoConfig):
        self._client = client
        self._db = config.database
        self._collection = config.collection

    async def _get_users_film_rating(self, user_id: UUID, film_id: UUID) -> int | None:
        """Получение оценки конкретного фильма конкретным юзером"""

        collection = self._client[self._db][self._collection]
        film_rating = collection.find(
            {"film_id": str(film_id), "user_id": str(user_id), "action_type": ActionType.rating},
        )

        result = [rating async for rating in film_rating]

        if not result:
            return None

        return result[0]['action_data']['rate']

    async def _get_review_rating(self, review_id: str) -> dict[str, int]:
        """Получение рейтинга рецензии на основе лайков/дизлайков"""

        collection = self._client[self._db][self._collection]
        reactions = [
            reaction
            async for reaction in collection.find(
                {"action_type": ActionType.reaction, "action_data.parent_id": review_id},
            )
        ]

        counters: dict[str, int] = defaultdict(int)
        for reaction in reactions:
            if reaction['action_data']['reaction'] > 0:
                counters['count_likes'] += 1
            else:
                counters['count_dislikes'] += 1
            counters['rating'] += reaction['action_data']['reaction']

        return counters

    async def get_all_reviews_by_film_id(self, film_id: UUID) -> list[FilmReview]:
        collection = self._client[self._db][self._collection]
        reviews_cursor = collection.find({"film_id": str(film_id), "action_type": ActionType.comment})

        reviews = [review async for review in reviews_cursor]

        for review in reviews:
            film_rating_by_user = await self._get_users_film_rating(
                user_id=review['user_id'], film_id=review['film_id']
            )
            reactions = await self._get_review_rating(review_id=str(review['_id']))

            review = {
                **review,
                'film_rating_by_user': film_rating_by_user,
                "reactions": reactions,
            }

        return [FilmReview.map_review_from_mongo(review) for review in reviews]

    async def get_all_reviews_by_user_id(self, user_id: UUID) -> list[FilmReview]:
        collection = self._client[self._db][self._collection]
        reviews_cursor = collection.find({"user_id": str(user_id), "action_type": ActionType.comment})

        reviews = [review async for review in reviews_cursor]

        for review in reviews:
            film_rating_by_user = await self._get_users_film_rating(
                user_id=review['user_id'], film_id=review['film_id']
            )
            reactions = await self._get_review_rating(review_id=str(review['_id']))

            review = {
                **review,
                'film_rating_by_user': film_rating_by_user,
                "reactions": reactions,
            }

        return [FilmReview.map_review_from_mongo(review) for review in reviews]
