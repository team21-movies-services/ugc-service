from pydantic import Field
from pydantic_settings import BaseSettings


# Настройки Kafka
class KafkaConfig(BaseSettings):
    host: str = Field(default='localhost:9092,localhost:9093,localhost:9094', alias='KAFKA_HOST')


# Настройки ClickHouse
class ClickHouseConfig(BaseSettings):
    host: str = Field(default='localhost:8123', alias='CLICKHOUSE_HOST')
    user: str = Field(default='default', alias='CLICKHOUSE_USER')
    password: str = Field(default='1234', alias='CLICKHOUSE_PASSWORD')


class Settings(BaseSettings):
    kafka: KafkaConfig = KafkaConfig()
    click_house: ClickHouseConfig = ClickHouseConfig()


settings = Settings()


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'verbose'}},
    'loggers': {
        'etl': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
