from http import HTTPStatus

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorCollection

pytestmark = pytest.mark.asyncio


async def test_delete_comment(api_client: AsyncClient, mongo_collection: AsyncIOMotorCollection, make_comment):
    result = await mongo_collection.insert_one(make_comment)
    _id = str(result.inserted_id)
    json = {"action_type": "comment", "_id": _id}

    response = await api_client.request(url='/api/v1/actions/', method="DELETE", json=json)
    status = response.status_code

    assert status == HTTPStatus.NO_CONTENT

    response = await api_client.request(url='/api/v1/actions/', method="DELETE", json=json)
    status = response.status_code

    assert status == HTTPStatus.NOT_FOUND


async def test_delete_reaction(
    api_client: AsyncClient,
    mongo_collection: AsyncIOMotorCollection,
    make_reaction,
):
    await mongo_collection.insert_one(make_reaction)
    user_id = make_reaction.get("user_id")
    action_data = make_reaction.get("action_data")
    parent_id = action_data.get("parent_id") if isinstance(action_data, dict) else False
    json = {"action_type": "reaction", "user_id": user_id, "parent_id": parent_id}

    response = await api_client.request(url='/api/v1/actions/', method="DELETE", json=json)
    status = response.status_code

    assert status == HTTPStatus.NO_CONTENT

    response = await api_client.request(url='/api/v1/actions/', method="DELETE", json=json)
    status = response.status_code
    body = response.json()

    assert body == {"detail": "Action not found"}
    assert status == HTTPStatus.NOT_FOUND


async def test_delete_rating(
    api_client: AsyncClient,
    mongo_collection: AsyncIOMotorCollection,
    make_rating: dict,
):
    await mongo_collection.insert_one(make_rating)
    user_id = make_rating.get("user_id")
    action_data = make_rating.get("action_data")
    parent_id = action_data.get("parent_id") if isinstance(action_data, dict) else False
    json = {"action_type": "rating", "user_id": user_id, "parent_id": parent_id}
    response = await api_client.request(url='/api/v1/actions/', method="DELETE", json=json)
    status = response.status_code

    assert status == HTTPStatus.NO_CONTENT

    response = await api_client.request(url='/api/v1/actions/', method="DELETE", json=json)
    status = response.status_code
    body = response.json()

    assert body == {"detail": "Action not found"}
    assert status == HTTPStatus.NOT_FOUND


async def test_delete_favorite(
    api_client: AsyncClient,
    mongo_collection: AsyncIOMotorCollection,
    make_favorite: dict,
):
    await mongo_collection.insert_one(make_favorite)
    user_id = make_favorite.get("user_id")
    film_id = make_favorite.get("film_id")
    json = {"action_type": "favorite", "film_id": film_id, "user_id": user_id}

    response = await api_client.request(url='/api/v1/actions/', method="DELETE", json=json)
    status = response.status_code

    assert status == HTTPStatus.NO_CONTENT

    response = await api_client.request(url='/api/v1/actions/', method="DELETE", json=json)
    status = response.status_code
    body = response.json()

    assert body == {"detail": "Action not found"}
    assert status == HTTPStatus.NOT_FOUND
