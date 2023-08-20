from uuid import UUID
import logging

from fastapi import APIRouter, Depends

from dependencies.auth import get_auth_data
from schemas.domain.auth import AuthData

router = APIRouter(prefix='/films', tags=['Films'])
logger = logging.getLogger(__name__)


@router.get(
    '/{film_id}/rating',
    summary="Получить рейтинг фильма",
)
async def _get_film_rating(
    film_id: UUID,
    auth_data: AuthData = Depends(get_auth_data),
):
    return 100
