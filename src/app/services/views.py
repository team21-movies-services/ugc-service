from abc import ABC, abstractmethod

from clients.kafka.kafka_client import KafkaService, get_kafka_service
from fastapi import Depends
from pydantic import UUID4


class ViewsServiceABC(ABC):
    @abstractmethod
    async def save_view_data(self,
                             movie_id: UUID4,
                             user_id: UUID4,
                             viewed_frame: int):
        ...


class ViewsService(ViewsServiceABC):
    topic = "views"

    async def save_view_data(self,
                             movie_id: UUID4,
                             user_id: UUID4,
                             viewed_frame: int,
                             kafka_service: KafkaService = Depends(get_kafka_service())):
        key = f"{user_id}+{movie_id}"
        value = str(viewed_frame)

        kafka_service.send_message(topic=self.topic,
                                   key=key,
                                   value=value)

        return f"message to Kafka: {key}:{value}"
