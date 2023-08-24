from fastapi import FastAPI
from httpx import AsyncClient

from providers import BaseProvider


class HTTPXClientProvider(BaseProvider):
    def __init__(
        self,
        app: FastAPI,
    ):
        self.app = app
        self.http_client: AsyncClient | None = None

    async def startup(self):
        """FastAPI startup event"""
        self.http_client = AsyncClient()
        setattr(self.app.state, "async_http_client", self.http_client)

    async def shutdown(self):
        """FastAPI shutdown event"""
        ...
