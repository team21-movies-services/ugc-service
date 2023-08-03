import asyncio
import logging
import random
import uuid

from aiokafka import AIOKafkaProducer
from settings import settings

logger = logging.getLogger(__name__)


async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka.host)

    await producer.start()
    user_id = uuid.uuid4()
    movie_id = uuid.uuid4()
    key = f"{user_id}+{movie_id}".encode()
    viewed_frame = 1
    while True:
        try:
            # Produce messages
            viewed_frame += 1
            value = f"{viewed_frame}".encode()
            partition = random.choice(range(1, 4))  # noqa
            response = await producer.send_and_wait("views", value, key, partition)
            logger.error(response)
            await asyncio.sleep(0.5)
        except Exception:
            await producer.stop()
            raise


asyncio.run(send_one())
