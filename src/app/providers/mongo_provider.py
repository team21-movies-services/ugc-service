import logging

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from providers import BaseProvider

logger = logging.getLogger(__name__)


class MongoProvider(BaseProvider):
    def __init__(self, app: FastAPI, dsn: str):
        super().__init__(app)
        self.dsn = dsn
        self.mongo_client = AsyncIOMotorClient(self.dsn)

    async def startup(self):
        """FastAPI startup event"""

        try:
            response = await self.mongo_client.admin.command({'ping': 1})
            logger.info(f"Connected to mongo server. dsn={self.dsn} response={response}")
        except ServerSelectionTimeoutError as error:
            logger.error(f"Some error connect to mongo. See={self.dsn}\n{error}")

        setattr(self.app.state, "mongo_client", self.mongo_client)

    async def shutdown(self):
        """FastAPI shutdown event"""
        if self.mongo_client:
            self.mongo_client.close()

    def register_events(self):
        self.app.add_event_handler("startup", self.startup)
        self.app.add_event_handler("shutdown", self.shutdown)
