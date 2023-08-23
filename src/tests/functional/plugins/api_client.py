import pytest_asyncio
from functional.settings import Settings
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from dependencies.auth import get_auth_data
from dependencies.clients.mongo import get_mongo_client
from dependencies.clients.redis_client import get_redis_client
from dependencies.settings import get_settings
from main import app


@pytest_asyncio.fixture(name='mongo_client', scope='session')
async def mongo_client_fixture(settings: Settings):
    client = AsyncIOMotorClient(settings.mongo.dsn)
    yield client

    client.close()


@pytest_asyncio.fixture(name='mongo_collection', autouse=True)
async def get_mongo_collection(mongo_client: AsyncIOMotorClient, settings: Settings):
    collection = mongo_client[settings.mongo.database][settings.mongo.collection]
    yield collection
    await collection.delete_many({})


@pytest_asyncio.fixture(name="api_client", scope='session')
async def client_fixture(mongo_client, redis_client, auth_user, settings):
    def get_mongo_override():
        return mongo_client

    def get_redis_override():
        return redis_client

    def get_auth_override():
        return auth_user

    def get_settings_override():
        return settings

    app.dependency_overrides[get_mongo_client] = get_mongo_override
    app.dependency_overrides[get_redis_client] = get_redis_override
    app.dependency_overrides[get_auth_data] = get_auth_override
    app.dependency_overrides[get_settings] = get_settings_override
    async with AsyncClient(app=app, base_url="http://test", headers={"X-Request-Id": '123'}) as client:
        yield client
