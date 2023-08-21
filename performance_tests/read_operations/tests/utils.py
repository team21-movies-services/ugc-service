import logging
from functools import wraps
from time import time

logger = logging.getLogger(__name__)


def timer_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.warn(f"Начинаю выполнение функции {func.__name__}")
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        logger.warn(f"Выполнение функции {func.__name__} заняло {end_time - start_time} сек.")
        return result

    return wrapper
