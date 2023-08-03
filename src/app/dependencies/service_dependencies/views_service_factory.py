from aiokafka import AIOKafkaProducer
from fastapi import Depends

from clients.streamer.kafka import KafkaService
from dependencies.clients.kafka_client import get_kafka_producer
from dependencies.registrator import add_factory_to_mapper
from services.views import ViewsService, ViewsServiceABC


@add_factory_to_mapper(ViewsServiceABC)
def create_views_service(
    kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> ViewsService:
    event_streamer_service = KafkaService(kafka_producer)

    return ViewsService(event_streamer_service)
