from fastapi import FastAPI
from redis.asyncio import Redis

from core.exceptions import AppException
from providers import BaseProvider


class RedisProvider(BaseProvider):
    def __init__(
        self,
        app: FastAPI,
        host: str,
        port: int,
    ):
        self.app = app
        self.redis_client: Redis = Redis(host=host, port=port)

    async def startup(self):
        """FastAPI startup event"""
        # TODO: backoff

        if not await self.redis_client.ping():
            raise AppException()

        setattr(self.app.state, "async_redis_client", self.redis_client)

    async def shutdown(self):
        """FastAPI shutdown event"""
        if self.redis_client:
            await self.redis_client.close()
