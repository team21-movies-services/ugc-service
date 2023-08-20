from typing import AsyncGenerator

from fastapi import Depends, FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient

from clients.mongo_client import AsyncMongoClient
from core.config import Settings
from dependencies.settings import get_settings


async def get_mongo_client(request: Request) -> AsyncGenerator[AsyncIOMotorClient, None]:
    app: FastAPI = request.app
    mongo_client: AsyncIOMotorClient = app.state.mongo_client
    yield mongo_client


async def get_async_mongo_client(
    request: Request,
    settings: Settings = Depends(get_settings),
) -> AsyncGenerator[AsyncMongoClient, None]:
    app: FastAPI = request.app
    mongo_client: AsyncIOMotorClient = app.state.mongo_client
    async_mongo_client = AsyncMongoClient(
        mongo_client=mongo_client,
        mongo_config=settings.mongo,
    )
    yield async_mongo_client
