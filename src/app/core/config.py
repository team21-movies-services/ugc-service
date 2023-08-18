import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Настройки Mongo
class MongoConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='mongo_')
    host_1: str = Field(default='mongos1')
    host_2: str = Field(default='mongos2')
    port_1: int = Field(default=27017)
    port_2: int = Field(default=27018)
    username: str = Field(default='default')
    password: str = Field(default='default')

    database: str = Field(default='film_events')
    collection: str = Field(default='film_events')

    @property
    def dsn(self):
        return f"mongodb://{self.host_1}:{self.port_1},{self.host_2}:{self.port_2}"


# Настройки Redis
class RedisConfig(BaseSettings):
    port: int = Field(default=6379, alias='REDIS_PORT')
    host: str = Field(default='127.0.0.1', alias='REDIS_HOST')


# Настройки Kafka
class KafkaConfig(BaseSettings):
    host: str = Field(default=..., alias='KAFKA_HOST')


# Настройки Sentry
class SentryConfig(BaseSettings):
    dsn: str = Field(default=..., alias='SENTRY_DSN')
    enable: bool = Field(default=True, alias='SENTRY_ENABLE')


# Название проекта. Используется в Swagger-документации
class ProjectConfig(BaseSettings):
    name: str = Field(default='ugc_service_api', alias='PROJECT_NAME')
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')
    jwt_secret_key: str = Field(default=..., alias='JWT_SECRET_KEY')


class Settings(BaseSettings):
    project: ProjectConfig = ProjectConfig()
    redis: RedisConfig = RedisConfig()
    kafka: KafkaConfig = KafkaConfig()
    sentry: SentryConfig = SentryConfig()
    mongo: MongoConfig = MongoConfig()


settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
