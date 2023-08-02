from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from providers import BaseProvider


class KafkaProvider(BaseProvider):
    def __init__(
        self,
        app: FastAPI,
        host: str,
    ):
        self.app = app
        self.host = host

    async def startup(self):
        """FastAPI startup event"""

        self.kafka_producer: AIOKafkaProducer = AIOKafkaProducer(bootstrap_servers=self.host,
                                                                 max_batch_size=163840)

        await self.kafka_producer.start()

        setattr(self.app.state, "kafka_producer", self.kafka_producer)

    async def shutdown(self):
        """FastAPI shutdown event"""

        if self.kafka_producer:
            await self.kafka_producer.stop()
