from http import HTTPStatus

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import InsertOneResult

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    ("test_input", "expected_status"),
    [
        ({"action_type": "comment", "text": "Some new text"}, HTTPStatus.OK),
        ({"action_type": "comment", "text": "Some new text", "extra_field": 0}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
async def test_update_comment(
    api_client: AsyncClient,
    mongo_collection: AsyncIOMotorCollection,
    test_input: dict,
    make_comment: dict,
    expected_status: HTTPStatus,
):
    result: InsertOneResult = await mongo_collection.insert_one(make_comment)
    test_input["_id"] = str(result.inserted_id)

    response = await api_client.patch(url='/api/v1/actions/', json=test_input)
    status = response.status_code
    assert status == expected_status

    # new_comment = await mongo_collection.find_one({"_id": result.inserted_id}) or {}
    # new_text = new_comment.get('action_data').get('text')
    #
    # assert new_text == "Some new text"


@pytest.mark.parametrize(
    ("test_input", "expected_status"),
    [
        (
            {
                "action_type": "reaction",
                "reaction": -1,
            },
            HTTPStatus.OK,
        ),
        ({"action_type": "reaction", "reaction": -1, "extra_field": 0}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
async def test_update_reaction(
    api_client: AsyncClient,
    mongo_collection: AsyncIOMotorCollection,
    test_input: dict,
    make_reaction: dict,
    expected_status: HTTPStatus,
):
    await mongo_collection.insert_one(make_reaction)
    user_id = make_reaction.get("user_id")
    action_data = make_reaction.get("action_data")
    parent_id = action_data.get("parent_id") if isinstance(action_data, dict) else False
    test_input.update({"user_id": user_id, "parent_id": parent_id})

    response = await api_client.patch(url='/api/v1/actions/', json=test_input)

    status = response.status_code
    assert status == expected_status


@pytest.mark.parametrize(
    ("test_input", "expected_status"),
    [
        (
            {
                "action_type": "rating",
                "rate": 10,
            },
            HTTPStatus.OK,
        ),
        ({"action_type": "rating", "rate": 10, "extra_field": 0}, HTTPStatus.UNPROCESSABLE_ENTITY),
    ],
)
async def test_update_rating(
    api_client: AsyncClient,
    mongo_collection: AsyncIOMotorCollection,
    test_input: dict,
    make_rating: dict,
    expected_status: HTTPStatus,
):
    await mongo_collection.insert_one(make_rating)
    user_id = make_rating.get("user_id")
    action_data = make_rating.get("action_data")
    parent_id = action_data.get("parent_id") if isinstance(action_data, dict) else False
    test_input.update({"user_id": user_id, "parent_id": parent_id})

    response = await api_client.patch(url='/api/v1/actions/', json=test_input)
    status = response.status_code
    assert status == expected_status
