from uuid import UUID
import logging

from fastapi import APIRouter, Depends

from dependencies.auth import get_auth_data
from schemas.domain.auth import AuthData
from schemas.response.rating import FilmRating

from services.rating import RatingServiceABC

router = APIRouter(prefix='/films', tags=['Films'])
logger = logging.getLogger().getChild('rating-router')


@router.get(
    '/{film_id}/rating',
    summary="Получить рейтинг фильма",
)
async def _get_film_rating(
    film_id: UUID,
    auth_data: AuthData = Depends(get_auth_data),
    rating_service: RatingServiceABC = Depends(),
) -> FilmRating:
    return await rating_service.get_film_rating(film_id)
