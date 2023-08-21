import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from dependencies.auth import get_auth_data
from schemas.domain.auth import AuthData
from schemas.response.reviews import FilmReview
from services.reviews import ReviewsServiseABC

router = APIRouter(prefix='/reviews', tags=['Reviews'])

logger = logging.getLogger().getChild('reviews-router')


@router.get(
    '/{film_id}',
    summary="Получение списка рецензий к фильму по id фильма",
    response_model=list[FilmReview],
)
async def get_film_reviews_by_id(
    film_id: UUID,
    sort_by: Optional[str] = Query(None, description='Сортировка рецензий по дате или рейтингу'),
    auth_data: AuthData = Depends(get_auth_data),
    reviews_service: ReviewsServiseABC = Depends(),
) -> list[FilmReview]:
    return await reviews_service.get_reviews_by_film_id(
        film_id=film_id,
        sort_by=sort_by,
    )


@router.get(
    '/user/',
    summary="Получение списка рецензий пользователя",
    response_model=list[FilmReview],
)
async def get_film_reviews_by_user(
    sort_by: Optional[str] = Query(None, description='Сортировка рецензий по дате или рейтингу'),
    auth_data: AuthData = Depends(get_auth_data),
    reviews_service: ReviewsServiseABC = Depends(),
) -> list[FilmReview]:
    return await reviews_service.get_reviews_by_user_id(
        user_id=auth_data.user_id,
        sort_by=sort_by,
    )
