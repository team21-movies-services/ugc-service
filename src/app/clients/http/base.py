from abc import ABC, abstractmethod
from typing import Any


class AsyncHTTPClientABC(ABC):
    @abstractmethod
    async def get(
        self,
        path: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def post(
        self,
        path: str,
        headers: dict | None = None,
        data: dict | None = None,
        params: dict | None = None,
    ) -> Any:
        raise NotImplementedError
