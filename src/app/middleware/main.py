import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from middleware.request_id import RequestIdHeaderMiddleware
from middleware.request_log import RequestLogMiddleware

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex='.*',
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestIdHeaderMiddleware)
    logger.info("Add RequestIdHeaderMiddleware middleware")

    app.add_middleware(RequestLogMiddleware)
    logger.info("Add RequestLogMiddleware middleware")
