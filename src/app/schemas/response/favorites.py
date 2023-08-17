from typing import Any, Mapping

from pydantic import UUID4, BaseModel

from core.exceptions.mongo import BadCollectionResponseException


class FavoriteMovie(BaseModel):
    film_id: UUID4
    action_time: int

    @classmethod
    def map_from_mongo(cls, favorite: Mapping[str, Any]) -> 'FavoriteMovie':
        film_id = favorite.get("film_id")
        action_time = favorite.get("action_time")
        if not film_id or not action_time:
            raise BadCollectionResponseException
        return FavoriteMovie(film_id=film_id, action_time=action_time)
