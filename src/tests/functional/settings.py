from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class TestMongoConfig(BaseSettings):
    host: str = Field(default=..., alias="MONGO_HOST")
    port: int = Field(default=..., alias="MONGO_PORT")

    database: str = Field(default='test_film_events')
    collection: str = Field(default='test_film_events')

    @property
    def dsn(self):
        return f"mongodb://{self.host}:{self.port}/?uuidRepresentation=standard"


class TestKafkaConfig(BaseSettings):
    host: str = Field(default="localhost", alias='KAFKA_HOST')


class TestProjectConfig(BaseSettings):
    name: str = Field(default='test_ugc_service_api', alias='PROJECT_NAME')
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')
    jwt_secret_key: str = "asdnjklnjkl123412bjk4bjk"


class TestRedisConfig(BaseSettings):
    port: int = Field(default=..., alias='REDIS_PORT')
    host: str = Field(default=..., alias='REDIS_HOST')


class TestSentryConfig(BaseSettings):
    dsn: str = Field(default="dsn", alias='SENTRY_DSN')
    enable: bool = Field(default=False, alias='SENTRY_ENABLE')


class Settings(BaseSettings):
    project: TestProjectConfig = TestProjectConfig()
    redis: TestRedisConfig = TestRedisConfig()
    kafka: TestKafkaConfig = TestKafkaConfig()
    sentry: TestSentryConfig = TestSentryConfig()
    mongo: TestMongoConfig = TestMongoConfig()


@lru_cache
def get_settings() -> Settings:
    return Settings()
