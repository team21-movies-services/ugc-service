from typing import AsyncGenerator

from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient


async def get_mongo_client(request: Request) -> AsyncGenerator[AsyncIOMotorClient, None]:
    app: FastAPI = request.app
    mongo_client: AsyncIOMotorClient = app.state.mongo_client
    yield mongo_client
