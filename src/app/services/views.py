from abc import ABC, abstractmethod

from clients.streamer.kafka import KafkaService
from pydantic import UUID4
from schemas.response.views import SaveViewDataResponse


class ViewsServiceABC(ABC):
    @abstractmethod
    async def save_view_data(self,
                             movie_id: UUID4,
                             user_id: UUID4,
                             viewed_frame: int) -> SaveViewDataResponse:
        ...


class ViewsService(ViewsServiceABC):
    topic = "views"

    def __init__(self, kafka_service: KafkaService):
        self._kafka_service = kafka_service

    async def save_view_data(self,
                             movie_id: UUID4,
                             user_id: UUID4,
                             viewed_frame: int) -> SaveViewDataResponse:

        key = f"{user_id}+{movie_id}"
        value = str(viewed_frame)

        await self._kafka_service.send_message(topic=self.topic,
                                               key=key,
                                               value=value)

        return SaveViewDataResponse(
            message="View data has sent to Kafka",
            user_id=user_id,
            movie_id=movie_id,
            viewed_frame=viewed_frame,
        )
