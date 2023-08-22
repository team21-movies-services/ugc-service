import pytest_asyncio
from functional.settings import get_settings
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from dependencies.auth import get_auth_data
from dependencies.clients.mongo import get_mongo_client
from dependencies.clients.redis_client import get_redis_client
from main import app

settings = get_settings()


@pytest_asyncio.fixture(name='mongo_client', scope='session')
async def mongo_client_fixture():
    client = AsyncIOMotorClient(settings.mongo.dsn)
    yield client

    client.close()


@pytest_asyncio.fixture(autouse=True)
async def clean_mongo_collection(mongo_client: AsyncIOMotorClient):
    collection = mongo_client[settings.mongo.database][settings.mongo.collection]
    await collection.delete_many({})


@pytest_asyncio.fixture(name="api_client", scope='session')
async def client_fixture(mongo_client, redis_client, auth_user):
    def get_mongo_override():
        return mongo_client

    def get_redis_override():
        return redis_client

    def get_auth_override():
        return auth_user

    app.dependency_overrides[get_mongo_client] = get_mongo_override
    app.dependency_overrides[get_redis_client] = get_redis_override
    app.dependency_overrides[get_auth_data] = get_auth_override
    async with AsyncClient(app=app, base_url="http://test", headers={"X-Request-Id": '123'}) as client:
        yield client
