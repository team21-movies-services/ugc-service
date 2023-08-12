from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from providers import BaseProvider


class MongoProvider(BaseProvider):
    def __init__(self, app: FastAPI, dsn: str):
        super().__init__(app)
        self.mongo_client: AsyncIOMotorClient | None = None
        self.dsn = dsn

    async def startup(self):
        """FastAPI startup event"""
        self.mongo_client = AsyncIOMotorClient(self.dsn)
        setattr(self.app.state, "mongo_client", self.mongo_client)

    async def shutdown(self):
        """FastAPI shutdown event"""
        if self.mongo_client:
            self.mongo_client.close()

    def register_events(self):
        self.app.add_event_handler("startup", self.startup)
        self.app.add_event_handler("shutdown", self.shutdown)
