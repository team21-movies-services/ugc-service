from http import HTTPStatus

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "test_input",
    [
        {
            "action_type": "rating",
            "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "parent_id": "64e3676cec293c29b50d38fc",
            "rate": 10,
        },
        {
            "action_type": "reaction",
            "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
            "parent_id": "64e3676cec293c29b50d38fc",
            "reaction": 1,
        },
        {"action_type": "comment", "_id": "64e3676cec293c29b50d38fc", "text": "Some comment text"},
    ],
)
async def test_update_action(api_client: AsyncClient, test_input):
    response = await api_client.patch(url='/api/v1/actions/', json=test_input)

    status = response.status_code

    assert status == HTTPStatus.NOT_FOUND
    # assert status == HTTPStatus.OK
