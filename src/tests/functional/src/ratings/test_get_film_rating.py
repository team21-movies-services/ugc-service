from http import HTTPStatus

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorCollection

from schemas.request.user_actions import Action
from schemas.response.rating import FilmRating

pytestmark = pytest.mark.asyncio


async def test_get_film_rating(
    api_client: AsyncClient,
    mongo_collection: AsyncIOMotorCollection,
    fake_action_film_rating: Action,
):
    await mongo_collection.insert_one(fake_action_film_rating.model_dump(by_alias=True, exclude_none=True))

    film_id = fake_action_film_rating.film_id
    response = await api_client.get(f'/api/v1/films/{film_id}/rating')
    assert response.status_code == HTTPStatus.OK

    film_rating = FilmRating.model_validate(response.json())

    assert film_rating.count_likes == 1
    assert film_rating.count_dislikes == 0
    assert film_rating.average_rating == 10.0
