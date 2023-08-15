import logging

from fastapi import APIRouter, Depends

from dependencies.auth import get_auth_data
from schemas.domain.auth import AuthData
from schemas.response.favorites import FavoriteMovie
from services.favorites import FavoritesServiceABC

router = APIRouter(prefix='/favorites', tags=['Favorites'])

logger = logging.getLogger().getChild('favorites-router')


@router.get(
    '',
    summary="Получить закладки пользователя",
    response_model=list[FavoriteMovie],
)
async def get_user_favorites(
    auth_data: AuthData = Depends(get_auth_data),
    favorites_service: FavoritesServiceABC = Depends(),
) -> list[FavoriteMovie]:
    return await favorites_service.get_favorites_by_user_id(user_id=auth_data.user_id)
