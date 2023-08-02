from clients.kafka.kafka_client import KafkaService, get_kafka_service
from dependencies.registrator import add_factory_to_mapper
from fastapi import Depends
from services.views import ViewsService, ViewsServiceABC


@add_factory_to_mapper(ViewsServiceABC)
def create_views_service(
    kafka_service: KafkaService = Depends(get_kafka_service),
) -> ViewsService:
    return ViewsService(kafka_service)
