import asyncio
import time

from aiokafka import AIOKafkaProducer


async def send_one():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092,localhost:9093,localhost:9094',
        max_batch_size=163840,
    )
    await producer.start()
    try:
        for _ in range(10):
            await producer.send("views", b"Super message", b"hi")
            time.sleep(1)
    finally:
        await producer.send("views", b"Goodbye message", b"bye")
        await producer.stop()


asyncio.run(send_one())
