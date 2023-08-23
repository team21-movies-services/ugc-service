from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from repositories.reviews import ReviewsRepositoryABC
from schemas.response.reviews import FilmReview


class ReviewsServiseABC(ABC):
    @abstractmethod
    async def _get_all_data_reviews(self, reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def _sort_reviews(self, sort_by: str, reviews: list[FilmReview]) -> list[FilmReview]:
        raise NotImplementedError

    @abstractmethod
    async def get_reviews_by_film_id(self, film_id: UUID, sort_by: str | None) -> list[FilmReview]:
        raise NotImplementedError

    @abstractmethod
    async def get_reviews_by_user_id(self, user_id: UUID, sort_by: str | None) -> list[FilmReview]:
        raise NotImplementedError


class ReviewsService(ReviewsServiseABC):
    def __init__(self, reviews_repository: ReviewsRepositoryABC) -> None:
        self._reviews_repository = reviews_repository

    async def _get_all_data_reviews(self, reviews: list[dict[str, Any]]) -> list[dict[str, Any]]:
        all_data_reviews = []

        for review in reviews:
            film_rating_by_user = await self._reviews_repository.get_users_film_rating(
                user_id=review['user_id'],
                film_id=review['film_id'],
            )
            reactions = await self._reviews_repository.get_review_rating(review_id=str(review['_id']))

            review = {
                **review,
                'film_rating_by_user': film_rating_by_user,
                "reactions": reactions,
            }
            all_data_reviews.append(review)

        return all_data_reviews

    async def _sort_reviews(self, sort_by: str, reviews: list[FilmReview]) -> list[FilmReview]:
        if sort_by == 'date':
            reviews = sorted(reviews, key=lambda review: review.action_time, reverse=True)
        elif sort_by == 'rating':
            reviews = sorted(reviews, key=lambda review: review.reactions.get('rating', 0), reverse=True)

        return reviews

    async def get_reviews_by_film_id(self, film_id: UUID, sort_by: str | None) -> list[FilmReview]:
        reviews = await self._reviews_repository.get_all_reviews_by_film_id(film_id)

        all_data_reviews = [
            FilmReview.map_review_from_mongo(review) for review in await self._get_all_data_reviews(reviews)
        ]

        if sort_by:
            all_data_reviews = await self._sort_reviews(sort_by=sort_by, reviews=all_data_reviews)

        return all_data_reviews

    async def get_reviews_by_user_id(self, user_id: UUID, sort_by: str | None) -> list[FilmReview]:
        reviews = await self._reviews_repository.get_all_reviews_by_user_id(user_id)

        all_data_reviews = [
            FilmReview.map_review_from_mongo(review) for review in await self._get_all_data_reviews(reviews)
        ]

        if sort_by:
            all_data_reviews = await self._sort_reviews(sort_by=sort_by, reviews=all_data_reviews)

        return all_data_reviews
