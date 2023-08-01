import asyncio
import logging.config

from settings import LOGGING, settings

from clients import KafkaConsumer

# from repository import ClickHouseRepository


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('etl')
logger.setLevel(logging.DEBUG)


async def run_etl(ev_loop: asyncio.AbstractEventLoop):
    kafka_consumer = KafkaConsumer(settings.kafka.host)
    # ch_repository = ClickHouseRepository(settings.click_house)

    movies_viewed_data = kafka_consumer.consumer_loop(topics=['views'], ev_loop=ev_loop)
    async for movies_data in movies_viewed_data:
        logger.debug(movies_data)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(run_etl(loop))
