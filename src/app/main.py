from logging import config as logging_config

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.routers.main import setup_routers
from core.config import Settings
from core.logger import LOGGING
from dependencies.main import setup_dependencies
from middleware.main import setup_middleware
from providers.main import setup_providers

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.project.name,
        docs_url='/docs',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
        description="User-Generated Content service",
        version="0.1.0",
    )
    setup_providers(app, settings)
    setup_routers(app)
    setup_dependencies(app)
    setup_middleware(app)
    return app


settings = Settings()
app = create_app(settings)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',  # noqa
        port=8001,
        reload=True,
    )
