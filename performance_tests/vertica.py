from typing import Any, Iterable

import vertica_python
from tqdm import tqdm
from vertica_python import Connection

from utils import gen_data, timer_dec

BATCH_SIZE: int = 1000
BATCH_AMOUNT: int = 100
TABLE_NAME: str = 'views'


@timer_dec
def create_table(connection: Connection) -> None:
    cursor = connection.cursor()
    cursor.execute(
        f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id IDENTITY,
                user_id VARCHAR(256) NOT NULL,
                film_id VARCHAR(256) NOT NULL,
                viewed_frame INTEGER NOT NULL,
                created_at INTEGER NOT NULL
            );
        """,
    )
    cursor.close()


@timer_dec
def clear_table(connection: Connection) -> None:
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {TABLE_NAME}")
    cursor.close()


@timer_dec
def write_test(data: Iterable[list[dict[str, Any]]], connection: Connection) -> None:
    cursor = connection.cursor()
    for batch in tqdm(data, total=BATCH_AMOUNT):
        cursor.executemany(
            f"""
                INSERT INTO {TABLE_NAME}(user_id, film_id, viewed_frame, created_at)
                    VALUES (:user_id, :film_id, :viewed_frame, :created_at); COMMIT;
            """,
            batch,
        )
    cursor.close()


@timer_dec
def read_test(connection: Connection) -> None:
    cursor = connection.cursor()
    cursor.execute(f'select * from {TABLE_NAME}')
    for _ in tqdm(cursor.iterate(), total=BATCH_AMOUNT * BATCH_SIZE):
        continue
    cursor.close()


def main():
    connection_info = {
        'host': '127.0.0.1',
        'port': 5433,
        'user': 'dbadmin',
        'password': '',
        'autocommit': True,
    }

    with vertica_python.connect(**connection_info) as connection:
        create_table(connection)
        clear_table(connection)
        data_gen = gen_data(BATCH_SIZE, BATCH_AMOUNT)
        write_test(data_gen, connection)
        read_test(connection)


if __name__ == '__main__':
    main()
