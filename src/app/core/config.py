import os

from pydantic import Field
from pydantic_settings import BaseSettings


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


settings = Settings()

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
