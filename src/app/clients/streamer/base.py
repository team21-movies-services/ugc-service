from abc import ABC, abstractmethod


class EventStreamerServiceABC(ABC):
    @abstractmethod
    async def send_message(self, topic: str, key: str, value: int) -> None:
        raise NotImplementedError
