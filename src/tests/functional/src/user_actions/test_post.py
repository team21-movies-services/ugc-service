from http import HTTPStatus
from uuid import UUID

import pytest
from bson import ObjectId
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "test_input",
    [
        {
            "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "film_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "action_type": "comment",
            "action_time": 1122,
            "action_data": {
                "parent_type": "film",
                "parent_id": "64e3676cec293c29b50d38fc",
                "text": "Some comment text",
            },
        },
        {
            "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "film_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "action_type": "favorite",
            "action_time": 0,
        },
        {
            "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "film_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "action_type": "reaction",
            "action_time": 0,
            "action_data": {"parent_type": "film", "parent_id": "64e3676cec293c29b50d38fc", "reaction": 1},
        },
        {
            "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "film_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "action_type": "rating",
            "action_time": 10,
            "action_data": {"parent_type": "film", "parent_id": "64e3676cec293c29b50d38fc", "rate": 10},
        },
    ],
)
async def test_create_action(api_client: AsyncClient, test_input):
    response = await api_client.post('/api/v1/actions', json=test_input)

    status = response.status_code
    body = response.json()

    assert status == HTTPStatus.CREATED
    assert ObjectId.is_valid(body['action_id'])
    try:
        assert UUID(body['user_id']).version == 4
    except ValueError:
        pytest.fail('user_id is not valid UUID4')
