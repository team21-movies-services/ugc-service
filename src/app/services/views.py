from abc import ABC, abstractmethod

from pydantic import UUID4

from clients.streamer.base import EventStreamerServiceABC
from schemas.response.views import SaveViewDataResponse


class ViewsServiceABC(ABC):
    @abstractmethod
    async def save_view_data(self, movie_id: UUID4, user_id: UUID4, viewed_frame: int) -> SaveViewDataResponse:
        ...


class ViewsService(ViewsServiceABC):
    topic = "views"

    def __init__(self, event_streamer_service: EventStreamerServiceABC):
        self._event_streamer_service = event_streamer_service

    async def save_view_data(self, movie_id: UUID4, user_id: UUID4, viewed_frame: int) -> SaveViewDataResponse:
        """Реализация передачи сообщений в streamer service.
        В текущей реализации используется Apache Kafka"""

        key = f"{user_id}+{movie_id}"
        value = str(viewed_frame)

        await self._event_streamer_service.send_message(topic=self.topic, key=key, value=value)

        return SaveViewDataResponse(
            message="View data has sent to Kafka",
            user_id=user_id,
            movie_id=movie_id,
            viewed_frame=viewed_frame,
        )
