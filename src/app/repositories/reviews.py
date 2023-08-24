from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Any, Mapping
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import MongoConfig
from schemas.request.user_actions import ActionType


class ReviewsRepositoryABC(ABC):
    @abstractmethod
    async def get_all_reviews_by_film_id(
        self,
        film_id: UUID,
        page_size: int,
        page_number: int,
    ) -> list[Mapping[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def get_users_film_rating(self, user_id: UUID, film_id: UUID) -> int | None:
        """Получение оценки конкретного фильма конкретным юзером"""
        raise NotImplementedError

    @abstractmethod
    async def get_review_rating(self, review_id: str) -> dict[str, int]:
        """Получение рейтинга рецензии на основе лайков/дизлайков"""
        raise NotImplementedError

    @abstractmethod
    async def get_all_reviews_by_user_id(
        self,
        user_id: UUID,
        page_size: int,
        page_number: int,
    ) -> list[Mapping[str, Any]]:
        raise NotImplementedError


class ReviewsMongoRepository(ReviewsRepositoryABC):
    def __init__(self, client: AsyncIOMotorClient, config: MongoConfig):
        self._client = client
        self._db = config.database
        self._collection = config.collection

    async def get_users_film_rating(self, user_id: UUID, film_id: UUID) -> int | None:
        """Получение оценки конкретного фильма конкретным юзером"""

        collection = self._client[self._db][self._collection]
        film_rating = collection.find(
            {"film_id": str(film_id), "user_id": str(user_id), "action_type": ActionType.rating},
        )

        result = [rating async for rating in film_rating]

        if not result:
            return None

        return result[0]['action_data']['rate']

    async def get_review_rating(self, review_id: str) -> dict[str, int]:
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

    async def get_all_reviews_by_film_id(
        self,
        film_id: UUID,
        page_size: int,
        page_number: int,
    ) -> list[Mapping[str, Any]]:
        collection = self._client[self._db][self._collection]
        reviews_cursor = (
            collection.find({"film_id": str(film_id), "action_type": ActionType.comment})
            .limit(page_size)
            .skip(page_size * page_number)
        )

        return [review async for review in reviews_cursor]

    async def get_all_reviews_by_user_id(
        self,
        user_id: UUID,
        page_size: int,
        page_number: int,
    ) -> list[Mapping[str, Any]]:
        collection = self._client[self._db][self._collection]
        reviews_cursor = (
            collection.find({"user_id": str(user_id), "action_type": ActionType.comment})
            .limit(page_size)
            .skip(page_size * page_number)
        )

        return [review async for review in reviews_cursor]
