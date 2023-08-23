import logging
from abc import ABC, abstractmethod
from uuid import UUID

from repositories.rating import RatingRepositoryABC
from schemas.domain.film import FilmRatingDomain

logger = logging.getLogger().getChild('rating-service')


class RatingServiceABC(ABC):
    @abstractmethod
    async def get_film_rating(self, film_id: UUID) -> FilmRatingDomain:
        """Получение рейтинга фильма: кол-ва лайков и дизлайков, средняя оценка фильма"""
        raise NotImplementedError


class RatingService(RatingServiceABC):
    def __init__(self, rating_repository: RatingRepositoryABC):
        self._rating_repository = rating_repository

    async def get_film_rating(self, film_id: UUID) -> FilmRatingDomain:
        rates = await self._rating_repository.get_film_rates(film_id)
        logger.info(f"Get list of rates by film_id=[{film_id}] from repository = {rates}")

        rating_domain = FilmRatingDomain()
        async for rate in rates:
            if rate == 10:
                rating_domain.count_likes += 1
            elif rate == 0:
                rating_domain.count_dislikes += 1
            rating_domain.total += 1
            rating_domain.summary += rate

        return rating_domain
