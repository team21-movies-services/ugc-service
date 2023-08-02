from typing import AsyncGenerator

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI, Request


async def get_kafka_producer(
    request: Request,
) -> AsyncGenerator[AIOKafkaProducer, None]:
    app: FastAPI = request.app
    kafka_producer: AIOKafkaProducer = app.state.kafka_producer

    yield kafka_producer
