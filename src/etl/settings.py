from pydantic_settings import BaseSettings, SettingsConfigDict


# Настройки Kafka
class KafkaConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='KAFKA_', case_sensitive=False)

    host: str = 'localhost:9092,localhost:9093,localhost:9094'


# Настройки ClickHouse
class ClickHouseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='CLICKHOUSE_', case_sensitive=False)

    password: str = "1234"
    host: str = 'localhost'
    port: str = 'localhost'
    user: str = 'default'
    database: str = 'default'
    connect_timeout: int = 1000


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
