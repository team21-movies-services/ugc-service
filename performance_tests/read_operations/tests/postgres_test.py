from typing import Iterable
from uuid import UUID

import psycopg
from config import Config
from gen_data import gen_user_actions_data
from psycopg.rows import dict_row
from tqdm import tqdm

from schemas.request.user_actions import ActionType
from utils import timer_dec

BATCH_SIZE: int = 1000
BATCH_AMOUNT: int = 500

config = Config()
connect = psycopg.connect(**config.postgres_dsn, row_factory=dict_row)


@timer_dec
def write_test(data: Iterable) -> list[UUID]:
    sql = 'INSERT INTO users_favorites ("user_id", "film_id") VALUES (%s, %s) RETURNING user_id'
    users = []
    for batch in tqdm(data, total=BATCH_AMOUNT):
        with connect.cursor() as cursor:
            rows = [(item.user_id, item.film_id) for item in batch]
            cursor.executemany(sql, rows)
            users.append(rows[0][0])
        connect.commit()
    return users


@timer_dec
def read_test(data: list[UUID]) -> None:
    sql = 'SELECT film_id FROM users_favorites WHERE user_id = %s'
    with connect.cursor() as cursor:
        for user_id in tqdm(data, total=len(data)):
            cursor.execute(sql, [user_id]).fetchall()


if __name__ == '__main__':
    action_batch = gen_user_actions_data(action=ActionType.favorite, batch_size=BATCH_SIZE, batch_amount=BATCH_AMOUNT)
    read_test(write_test(action_batch))
