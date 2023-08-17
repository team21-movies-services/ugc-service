from abc import ABC, abstractmethod
from uuid import UUID

from repositories.favorites import FavoritesRepositoryABC
from schemas.response.favorites import FavoriteMovie


class FavoritesServiceABC(ABC):
    @abstractmethod
    async def get_favorites_by_user_id(self, user_id: UUID) -> list[FavoriteMovie]:
        raise NotImplementedError


class FavoritesService(FavoritesServiceABC):
    def __init__(self, favortie_repository: FavoritesRepositoryABC):
        self._favortie_repository = favortie_repository

    async def get_favorites_by_user_id(self, user_id: UUID) -> list[FavoriteMovie]:
        return await self._favortie_repository.get_favorites_by_user_id(user_id)
