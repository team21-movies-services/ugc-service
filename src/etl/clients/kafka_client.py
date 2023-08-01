import asyncio

from aiokafka import AIOKafkaConsumer, ConsumerRecord, TopicPartition
from models import MovieViewed


class KafkaConsumer:
    def __init__(self, kafka_hosts: str) -> None:
        self._hosts = kafka_hosts

    async def consumer_loop(self, ev_loop: asyncio.AbstractEventLoop, topics: list[str]):
        consumer = AIOKafkaConsumer(*topics, loop=ev_loop, bootstrap_servers=self._hosts, group_id="movie_viewed")
        try:
            await consumer.start()
            while True:
                for assignment in consumer.assignment():
                    partition: TopicPartition = assignment
                    await consumer.seek_to_end(partition)
                    response: dict[TopicPartition, list[ConsumerRecord]] = await consumer.getmany(
                        partition,
                        timeout_ms=1000,
                    )
                    if partition in response:
                        for record in response[partition]:
                            key: bytes = record.key or b''
                            value: bytes = record.value or b''
                            user_id, film_id = key.decode().split('+')
                            # TODO: return batch?
                            yield MovieViewed(
                                user_id=user_id,
                                film_id=film_id,
                                viewed_frame=int(value.decode()),
                            )
        finally:
            await consumer.stop()
