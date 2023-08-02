import asyncio
import logging
import random
import uuid

from aiokafka.producer import AIOKafkaProducer
from settings import settings

logger = logging.getLogger(__name__)


async def send_many(num):
    topic = "views"
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka.host)
    await producer.start()

    batch = producer.create_batch()

    i = 0
    viewed_frame = 1
    while i < num:
        user_id = uuid.uuid4()
        movie_id = uuid.uuid4()
        key = f"{user_id}+{movie_id}".encode()
        viewed_frame += 1
        value = f"{viewed_frame}".encode()
        metadata = batch.append(key=key, value=value, timestamp=None)
        if metadata is None:
            partitions = await producer.partitions_for(topic)
            partition = random.choice(tuple(partitions))  # noqa
            await producer.send_batch(batch, topic, partition=partition)
            logger.error("%d messages sent to partition %d" % (batch.record_count(), partition))
            batch = producer.create_batch()
            continue
        i += 1
    partitions = await producer.partitions_for(topic)
    partition = random.choice(tuple(partitions))  # noqa
    await producer.send_batch(batch, topic, partition=partition)
    logger.error("%d messages sent to partition %d" % (batch.record_count(), partition))
    await producer.stop()


asyncio.run(send_many(10_000_00))
