from http import HTTPStatus

import pytest
from httpx import AsyncClient

from schemas.response.rating import FilmRating

pytestmark = pytest.mark.asyncio


async def test_get_film_rating(api_client: AsyncClient, fake_action_film_rating):
    data = fake_action_film_rating.model_dump(by_alias=True, exclude_none=True)
    create_response = await api_client.post('/api/v1/actions', json=data)

    status = create_response.status_code
    assert status == HTTPStatus.CREATED

    film_id = fake_action_film_rating.film_id
    response = await api_client.get(f'/api/v1/films/{film_id}/rating')
    assert response.status_code == HTTPStatus.OK

    film_rating = FilmRating.model_validate(response.json())

    assert film_rating.count_likes == 1
