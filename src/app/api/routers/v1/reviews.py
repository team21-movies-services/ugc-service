import logging
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
    page_size: int = Query(10, description="Количество элементов на странице", ge=1),
    page_number: int = Query(0, description="Номер страницы", ge=0),
    sort_by: str | None = Query(None, description='Сортировка рецензий по дате или рейтингу'),
    auth_data: AuthData = Depends(get_auth_data),
    reviews_service: ReviewsServiseABC = Depends(),
) -> list[FilmReview]:
    return await reviews_service.get_reviews_by_film_id(
        film_id=film_id,
        sort_by=sort_by,
        page_size=page_size,
        page_number=page_number,
    )


@router.get(
    '/user/',
    summary="Получение списка рецензий пользователя",
    response_model=list[FilmReview],
)
async def get_film_reviews_by_user(
    page_size: int = Query(10, description="Количество элементов на странице", ge=1),
    page_number: int = Query(0, description="Номер страницы", ge=0),
    sort_by: str | None = Query(None, description='Сортировка рецензий по дате или рейтингу'),
    auth_data: AuthData = Depends(get_auth_data),
    reviews_service: ReviewsServiseABC = Depends(),
) -> list[FilmReview]:
    return await reviews_service.get_reviews_by_user_id(
        user_id=auth_data.user_id,
        sort_by=sort_by,
        page_size=page_size,
        page_number=page_number,
    )
