from http import HTTPStatus

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "test_input",
    [
        {"action_type": "comment", "_id": "64e3d156f20cc6923d663806"},
        {
            "action_type": "favorite",
            "user_id": "4bc7233d-c83e-4b6a-afc3-d025ecdf2397",
            "film_id": "4bc7233d-c83e-4b6a-afc3-d025ecdf2397",
        },
        {
            "action_type": "reaction",
            "user_id": "42c7233d-c833-4b6a-afc3-d025ecdf2397",
            "parent_id": "24e3676cec233c29b50d33fc",
        },
        {
            "action_type": "rating",
            "user_id": "4b37233d-c83e-4b6a-afc3-d025ecdf2397",
            "parent_id": "4b37233d-c83e-4b6a-afc3-d025ecdf2397",
        },
    ],
)
async def test_delete_action(api_client: AsyncClient, test_input):
    response = await api_client.request(url='/api/v1/actions/', method='DELETE', json=test_input)

    status = response.status_code

    assert status == HTTPStatus.NOT_FOUND
    # assert status == HTTPStatus.NO_CONTENT
