import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorCollection

pytestmark = pytest.mark.asyncio


async def test_get_favorites(api_client: AsyncClient, mongo_collection: AsyncIOMotorCollection, make_my_favorite: dict):
    await mongo_collection.insert_one(make_my_favorite)

    response = await api_client.get('/api/v1/favorites')
    status_code = response.status_code

    assert response.status_code == status_code
    for body in response.json():
        assert body["film_id"] == make_my_favorite["film_id"]
        assert body["action_time"] == make_my_favorite["action_time"]


async def test_get_favorites_empty(api_client: AsyncClient):
    response = await api_client.get('/api/v1/favorites')
    status_code = response.status_code

    assert response.status_code == status_code
    assert response.json() == []


async def test_get_only_my_favorites(
    api_client: AsyncClient,
    mongo_collection: AsyncIOMotorCollection,
    make_my_favorite: dict,
    make_favorite: dict,
):
    await mongo_collection.insert_many([make_my_favorite, make_favorite])

    response = await api_client.get('/api/v1/favorites')
    status_code = response.status_code

    assert response.status_code == status_code
    for body in response.json():
        assert body["film_id"] == make_my_favorite["film_id"]
        assert body["action_time"] == make_my_favorite["action_time"]
