import logging
from typing import AsyncGenerator

from clickhouse_driver import Client
from models import MovieViewed
from settings import ClickHouseConfig

logger = logging.getLogger().getChild('etl')


class ClickHouseRepository:
    def __init__(
        self,
        click_house_cfg: ClickHouseConfig,
    ) -> None:
        self._repository = self.get_client(click_house_cfg)

    @staticmethod
    def get_client(click_house_cfg: ClickHouseConfig):
        clickhouse_connection_options = {
            'host': click_house_cfg.host,
            'port': click_house_cfg.port,
            'database': click_house_cfg.database,
            'user': click_house_cfg.user,
            'password': click_house_cfg.password,
            'connect_timeout': click_house_cfg.connect_timeout,
        }
        return Client(**clickhouse_connection_options)

    async def save_movie_viewed(self, movies_viewed_data: AsyncGenerator[list[MovieViewed], None]):
        stmt = "INSERT INTO views (user_id, film_id, viewed_frame, event_time) VALUES"
        async for batch in movies_viewed_data:
            data = [movie.transform_for_clickhouse() for movie in batch]
            logger.info("Try load data to click house %s", data)
            result = self._repository.execute(stmt, data)
            logger.info("Save result %d", result)
