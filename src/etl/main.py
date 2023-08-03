import asyncio
import logging.config

from repository import ClickHouseRepository
from settings import LOGGING, settings

from clients import KafkaConsumer

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('etl')
logger.setLevel(logging.DEBUG)


async def run_etl(ev_loop: asyncio.AbstractEventLoop):
    kafka_consumer = KafkaConsumer(hosts=settings.kafka.host, topics=['views'], ev_loop=ev_loop)
    ch_repository = ClickHouseRepository(settings.click_house)

    movies_viewed_data = kafka_consumer.consumer_partition_loop()
    await ch_repository.save_movie_viewed(movies_viewed_data)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_etl(loop))
