from typing import Iterable

from clickhouse_driver import Client

from utils import gen_data, timer_dec

BATCH_SIZE: int = 1000
BATCH_AMOUNT: int = 10000
TABLE_NAME: str = 'default.views'

client = Client(host='localhost')


@timer_dec
def write_test(data: Iterable) -> None:
    for batch in data:
        client.execute(f'INSERT INTO {TABLE_NAME} VALUES ', batch)


@timer_dec
def read_test() -> None:
    pass


if __name__ == '__main__':
    data_gen = gen_data(BATCH_SIZE, BATCH_AMOUNT)
    write_test(data_gen)
    read_test()
