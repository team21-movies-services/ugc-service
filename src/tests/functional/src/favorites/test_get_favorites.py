from http import HTTPStatus

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_get_favorites(api_client: AsyncClient):
    response = await api_client.get('/api/v1/favorites')
    assert response.status_code == HTTPStatus.OK
