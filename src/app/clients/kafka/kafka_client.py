from aiokafka import AIOKafkaProducer


class KafkaService:
    def __init__(self):
        self.producer = None

    async def start(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers='localhost:9092,localhost:9093,localhost:9094',
            max_batch_size=163840)

        await self.producer.start()

    async def send_message(self, topic: str, key: str, value: int):
        await self.producer.send(topic=topic,
                                 key=key,
                                 value=value)

    async def close(self):
        if self.producer:
            await self.producer.stop()


async def get_kafka_service():
    kafka_service = KafkaService()
    await kafka_service.start()
    try:
        yield kafka_service
    finally:
        await kafka_service.close()
