from aiokafka import AIOKafkaProducer

from clients.streamer.base import StreamerServiceABC


class KafkaService(StreamerServiceABC):
    def __init__(self, producer: AIOKafkaProducer) -> None:
        self.producer = producer

    async def send_message(self, topic: str, key: str, value: int) -> None:
        # Отправка данных в Apache Kafka
        await self.producer.send(topic=topic,
                                 key=bytes(key, encoding='utf-8'),
                                 value=bytes(str(value), encoding='utf-8'))
