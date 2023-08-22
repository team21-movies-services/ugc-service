from uuid import uuid4

import pytest_asyncio

from schemas.domain.auth import AuthData


@pytest_asyncio.fixture(name='auth_user', scope='session')
async def auth_user_fixture():
    yield AuthData(user_id=uuid4(), is_superuser=False)
