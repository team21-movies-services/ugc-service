from http import HTTPStatus

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorCollection

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ("film_id", "params", "expected_length", "expected_status"),
    [
        ('998ba1aa-725d-4db3-b928-a5d6fad38fb3', {"page": 0, "size": 25}, 10, HTTPStatus.OK),
        ('998ba1aa-725d-4db3-b928-a5d6fad38fb1', {"page": 0, "size": 25}, 0, HTTPStatus.OK),
    ],
)
async def test_get_reviews(
    api_client: AsyncClient,
    mongo_collection: AsyncIOMotorCollection,
    make_review_pack,
    film_id,
    params,
    expected_length,
    expected_status,
):
    await mongo_collection.insert_many(make_review_pack)

    response = await api_client.get(f'/api/v1/reviews/{film_id}')

    status = response.status_code
    body = response.json()

    assert len(body) == expected_length
    assert status == expected_status
