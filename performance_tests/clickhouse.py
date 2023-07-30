from typing import Iterable

from clickhouse_driver import Client
from tqdm import tqdm
from utils import gen_data, timer_dec

BATCH_SIZE: int = 1000
BATCH_AMOUNT: int = 10000
TABLE_NAME: str = 'views'

client = Client(host='localhost', password='123', database='default')


@timer_dec
def write_test(data: Iterable) -> None:
    for batch in tqdm(data, total=BATCH_AMOUNT):
        client.execute(f'INSERT INTO {TABLE_NAME} (user_id, film_id, viewed_frame, event_time) VALUES', batch)


@timer_dec
def read_test() -> None:
    client.execute(f'select * from {TABLE_NAME}')


if __name__ == '__main__':
    data_gen = gen_data(BATCH_SIZE, BATCH_AMOUNT)
    write_test(data_gen)
    read_test()
