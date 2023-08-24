import logging
from typing import Any, Callable

from fastapi import FastAPI

from dependencies.mapping import dependencies_map

logger = logging.getLogger(__name__)


def _pretty_log(dependencies: dict, indent=0) -> tuple:
    for key, value in dependencies.items():
        logger.info('\t' * indent + str(key))
        if isinstance(value, dict):
            _pretty_log(value, indent + 1)
        else:
            logger.info('\t' * (indent + 1) + str(value))
    return tuple(dependencies.keys())


def setup_dependencies(app: FastAPI, mapper: dict[Any, Callable] | None = None):
    """Переопределение интерфейсов реальными экземплярами фабрик классов"""
    if mapper is None:
        mapper = dependencies_map
    for interface, dependency in mapper.items():
        app.dependency_overrides[interface] = dependency
    logger.info("\nDependencies mapping: %s", _pretty_log(app.dependency_overrides))

    return None
