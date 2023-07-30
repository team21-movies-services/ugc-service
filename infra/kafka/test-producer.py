import asyncio

from aiokafka import AIOKafkaProducer


async def send_one():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092,localhost:9093,localhost:9094',
    )
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("views", b"Super message", b"hi")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()


asyncio.run(send_one())
