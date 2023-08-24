import logging
from uuid import UUID

from fastapi import APIRouter, Depends

from dependencies.auth import get_auth_data
from schemas.response.rating import FilmRating
from services.rating import RatingServiceABC

router = APIRouter(prefix='/films', tags=['Films'])
logger = logging.getLogger().getChild('rating-router')


@router.get(
    '/{film_id}/rating',
    summary="Получить рейтинг фильма",
    dependencies=[Depends(get_auth_data)],
)
async def _get_film_rating(
    film_id: UUID,
    rating_service: RatingServiceABC = Depends(),
) -> FilmRating:
    rating_domain = await rating_service.get_film_rating(film_id)

    average = 0.0
    if rating_domain.summary:
        average = float("{:.2f}".format(rating_domain.summary / rating_domain.total))

    return FilmRating(
        count_likes=rating_domain.count_likes,
        count_dislikes=rating_domain.count_dislikes,
        average_rating=average,
    )
