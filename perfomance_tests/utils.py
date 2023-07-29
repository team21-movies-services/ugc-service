import uuid
from datetime import datetime
from functools import wraps
from typing import Generator

from time import time


def timer_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Начинаю выполнение функции {func.__name__}")
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print(f"Выполнение функции {func.__name__} заняло {end_time - start_time} сек.")
        return result

    return wrapper


def gen_data(batch_size: int, batch_amount: int) -> Generator[list[dict], None, None]:
    """

    Args:
        :param batch_size: Размер пачки данных для вставки
        :param batch_amount: Количество таких пачек
    Returns:
        Генератор который возвращает списки словарей в формате:
                - "user_id" (UUID4):
                - "film_id" (UUID4):
                - "viewed_frame" (int): Просмотренный отрезок фильма(например секунда)
                - "created_at" (datetime): Время создания записи о просмотре (текущее время).
    """
    for _ in range(batch_amount):
        user_id = uuid.uuid4()
        film_id = uuid.uuid4()
        yield [
            {
                "user_id": user_id,
                "film_id": film_id,
                "viewed_frame": i,
                "event_time": datetime.now()
            } for i in range(batch_size)
        ]
