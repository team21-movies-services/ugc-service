from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4

from pydantic import UUID4

from repositories.favorites import FavoritesRepositoryABC
from schemas.response.favorites import FavoriteMovie


class FavoritesServiceABC(ABC):
    @abstractmethod
    async def get_favorites_by_user_id(self, user_id: UUID4) -> list[FavoriteMovie]:
        raise NotImplementedError


class FavoritesService(FavoritesServiceABC):
    def __init__(self, favortie_repository: FavoritesRepositoryABC):
        self._favortie_repository = favortie_repository

    async def get_favorites_by_user_id(self, user_id: UUID4) -> list[FavoriteMovie]:
        return [FavoriteMovie(movie_id=uuid4(), created_at=datetime.now())]
