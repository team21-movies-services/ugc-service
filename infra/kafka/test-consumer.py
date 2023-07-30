import asyncio

from aiokafka import AIOKafkaConsumer


async def consume():
    consumer = AIOKafkaConsumer(
        'views',
        bootstrap_servers='localhost:9092,localhost:9093,localhost:9094',
        group_id="test-consumer",
        auto_offset_reset='earliest',
    )
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)  # noqa
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()


asyncio.run(consume())
