from http import HTTPStatus

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_favorites_without_auth(api_client: AsyncClient, access_token: str):
    _ = access_token

    response = await api_client.get('/api/v1/favorites')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


async def test_favorites_with_bad_token(api_client: AsyncClient, forbidden_access_token: str):
    response = await api_client.get('/api/v1/favorites', headers={'Authorization': forbidden_access_token})

    assert response.status_code == HTTPStatus.FORBIDDEN


async def test_favorites_with_expire_token(api_client: AsyncClient, expire_access_token: str):
    response = await api_client.get('/api/v1/favorites', headers={'Authorization': expire_access_token})
    message = response.json()["detail"]["error"]["message"]

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert message == "Error validating access token: Session has expired"
