import logging
from abc import ABC, abstractmethod
from collections import defaultdict
from uuid import UUID

from repositories.rating import RatingRepositoryABC
from schemas.response.rating import FilmRating

logger = logging.getLogger().getChild('rating-service')


class RatingServiceABC(ABC):
    @abstractmethod
    async def get_film_rating(self, film_id: UUID):
        """Получение рейтинга фильма: кол-ва лайков и дизлайков, средняя оценка фильма"""
        raise NotImplementedError


class RatingService(RatingServiceABC):
    def __init__(self, rating_repository: RatingRepositoryABC):
        self._rating_repository = rating_repository

    async def get_film_rating(self, film_id: UUID) -> FilmRating:
        rates = await self._rating_repository.get_film_rates(film_id)
        logger.info(f"Get list of rates by film_id=[{film_id}] from repository = {rates}")

        counters: dict[str, int] = defaultdict(int)
        async for rate in rates:
            if rate == 10:
                counters['likes'] += 1
            elif rate == 0:
                counters['dislikes'] += 1
            counters['count'] += 1
            counters['sum'] += rate

        return FilmRating(
            count_likes=counters['likes'],
            count_dislikes=counters['dislikes'],
            average_rating=float(counters['sum'] / counters['count']),
        )
