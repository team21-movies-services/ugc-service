import asyncio
import logging
from typing import AsyncGenerator

from aiokafka import AIOKafkaConsumer, ConsumerRecord, TopicPartition
from models import MovieViewed

logger = logging.getLogger().getChild('etl')


class KafkaConsumer:
    def __init__(self, hosts: str, ev_loop: asyncio.AbstractEventLoop, topics: list[str]) -> None:
        self._hosts = hosts
        self._consumer = AIOKafkaConsumer(
            *topics,
            loop=ev_loop,
            bootstrap_servers=self._hosts,
            group_id="movie_viewed",
            enable_auto_commit=False,
            auto_offset_reset='latest',
        )

    async def consumer_loop(self) -> AsyncGenerator[MovieViewed, None]:
        """
        Основной цикл получения сообщений из кафки

        Args:
            -
        Returns:
            Генератор DTO MovieViewed
        """
        consumer = self._consumer
        try:
            await consumer.start()
            async for record in consumer:
                key: bytes = record.key or b''
                value: bytes = record.value or b''
                user_id, film_id = key.decode().split('+')
                yield MovieViewed(
                    user_id=user_id,
                    film_id=film_id,
                    viewed_frame=int(value.decode()),
                )
                await self._manual_commit(record.topic, record.partition, record.offset, consumer)
        finally:
            await consumer.stop()

    async def _manual_commit(self, topic: str, partition: int, offset: int, consumer: AIOKafkaConsumer) -> None:
        tp = TopicPartition(topic, partition)
        offset = offset + 1
        await consumer.commit({tp: offset})
        logger.debug(f"commited: tp - {tp} offset - {offset}")

    async def consumer_partition_loop(self) -> AsyncGenerator[MovieViewed, None]:
        """Цикл получения записей MovieViewed из кафки по партициям"""
        consumer = self._consumer
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
