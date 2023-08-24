import asyncio

import pytest
from functional.settings import get_settings

pytest_plugins = (
    "functional.plugins.api_client",
    "functional.plugins.redis_client",
    "functional.plugins.auth_user",
    "functional.testdata.user_actions",
    "functional.testdata.reviews",
)


@pytest.fixture(scope="session")
def settings():
    """Получение настроек для тестов."""
    return get_settings()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
