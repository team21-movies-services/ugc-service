import asyncio

from aiokafka import AIOKafkaConsumer, TopicPartition


async def consume():
    consumer = AIOKafkaConsumer(
        'views',
        bootstrap_servers='localhost:9092,localhost:9093,localhost:9094',
        group_id="test-consumer",
        enable_auto_commit=False,
        auto_offset_reset='latest',
    )
    await consumer.start()
    try:
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)  # noqa
            await _manual_commit(msg.topic, msg.partition, msg.offset, consumer)
    finally:
        await consumer.stop()


async def _manual_commit(topic: str, partition: int, offset: int, consumer: AIOKafkaConsumer) -> None:
    tp = TopicPartition(topic, partition)
    offset = offset + 1
    await consumer.commit({tp: offset})
    print(f"commited: tp - {tp} offset - {offset}")  # noqa


asyncio.run(consume())
