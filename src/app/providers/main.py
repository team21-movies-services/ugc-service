import logging

from fastapi import FastAPI

from core.config import Settings
from providers.cache_providers import RedisProvider
from providers.http_providers import HTTPXClientProvider
from providers.kafka_provider import KafkaProvider
from providers.sentry_provider import SentryProvider

logger = logging.getLogger(__name__)


def setup_providers(app: FastAPI, settings: Settings):
    redis_provider = RedisProvider(
        app=app,
        host=settings.redis.host,
        port=settings.redis.port,
    )
    redis_provider.register_events()
    logger.info(f"Setup Redis Provider. host:port: {settings.redis.host}:{settings.redis.port}")

    http_client = HTTPXClientProvider(app=app)
    http_client.register_events()
    logger.info(f"Setup Http Provider. {http_client}")

    kafka_provider = KafkaProvider(app=app, host=settings.kafka.host)
    kafka_provider.register_events()
    logger.info(f"Setup Kafka Provider. host: {settings.kafka.host}")

    if settings.sentry.enable:
        sentry_provider = SentryProvider(app=app, dsn=settings.sentry.dsn)
        sentry_provider.register_events()
        logger.info("Setup Sentry Provider.")
