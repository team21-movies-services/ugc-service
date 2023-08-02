from aiokafka import AIOKafkaProducer


class KafkaService:
    def __init__(self):
        self.producer = None

    async def start(self):
        servers = """ugc-service-kafka-broker-1:19092,
        ugc-service-kafka-broker-2:19093,
        ugc-service-kafka-broker-3:19094"""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=servers,
            max_batch_size=163840)

        await self.producer.start()

    async def send_message(self, topic: str, key: str, value: int):
        await self.producer.send(topic=topic,
                                 key=bytes(key, encoding='utf-8'),
                                 value=bytes(str(value), encoding='utf-8'))

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
