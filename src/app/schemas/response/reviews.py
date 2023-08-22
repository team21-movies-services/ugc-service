from typing import Any, Mapping

from pydantic import UUID4, BaseModel

from core.exceptions.mongo import BadCollectionResponseException


class FilmReview(BaseModel):
    film_id: UUID4
    user_id: UUID4
    action_time: int
    text: str
    film_rating_by_user: int | None
    reactions: dict | None

    @classmethod
    def map_review_from_mongo(cls, review: Mapping[str, Any]) -> 'FilmReview':
        film_id = review.get("film_id")
        user_id = review.get("user_id")
        action_time = review.get("action_time")
        action_data = review.get("action_data")
        film_rating_by_user = review.get("film_rating_by_user")
        reactions = review.get("reactions")

        if not film_id or not action_time or not user_id or not action_data:
            raise BadCollectionResponseException

        return FilmReview(
            film_id=film_id,
            user_id=user_id,
            action_time=action_time,
            text=action_data["text"],
            film_rating_by_user=film_rating_by_user,
            reactions=reactions,
        )
