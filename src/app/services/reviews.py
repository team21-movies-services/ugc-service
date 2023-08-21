from abc import ABC, abstractmethod
from uuid import UUID

from repositories.reviews import ReviewsRepositoryABC
from schemas.response.reviews import FilmReview


class ReviewsServiseABC(ABC):
    @abstractmethod
    async def get_reviews_by_film_id(
        self,
        film_id: UUID,
        sort_by_data: bool = False,
        sort_by_rating: bool = False,
    ) -> list[FilmReview]:
        raise NotImplementedError

    @abstractmethod
    async def get_reviews_by_user_id(
        self,
        user_id: UUID,
        sort_by_data: bool = False,
        sort_by_rating: bool = False,
    ) -> list[FilmReview]:
        raise NotImplementedError


class ReviewsService(ReviewsServiseABC):
    def __init__(self, reviews_repository: ReviewsRepositoryABC) -> None:
        self._reviews_repository = reviews_repository

    async def get_reviews_by_film_id(
        self,
        film_id: UUID,
        sort_by_data: bool = False,
        sort_by_rating: bool = False,
    ) -> list[FilmReview]:
        reviews = await self._reviews_repository.get_all_reviews_by_user_id(film_id)

        if sort_by_data:
            reviews = sorted(reviews, key=lambda review: review.action_time, reverse=True)
        elif sort_by_rating:
            reviews = sorted(reviews, key=lambda review: review.reactions.get('rating', 0), reverse=True)

        return reviews

    async def get_reviews_by_user_id(
        self,
        user_id: UUID,
        sort_by_data: bool = False,
        sort_by_rating: bool = False,
    ) -> list[FilmReview]:
        reviews = await self._reviews_repository.get_all_reviews_by_user_id(user_id)

        if sort_by_data:
            reviews = sorted(reviews, key=lambda review: review.action_time, reverse=True)
        elif sort_by_rating:
            reviews = sorted(reviews, key=lambda review: review.reactions.get('rating', 0), reverse=True)

        return reviews
