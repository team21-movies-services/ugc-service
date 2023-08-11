from typing import Iterable

from pymongo import MongoClient
from tqdm import tqdm

from utils import gen_data, timer_dec

BATCH_SIZE: int = 1000
BATCH_AMOUNT: int = 100

COLLECTION_NAME: str = 'film_event'
DB_NAME: str = "film_event"

uri = "mongodb://localhost:27019"

client: MongoClient = MongoClient(uri)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


@timer_dec
def write_test(data: Iterable) -> None:
    for batch in tqdm(data, total=BATCH_AMOUNT):
        collection.insert_many(batch)


@timer_dec
def read_test() -> None:
    for _ in tqdm(collection.find(), total=BATCH_AMOUNT * BATCH_SIZE):
        continue


if __name__ == '__main__':
    data_gen = gen_data(BATCH_SIZE, BATCH_AMOUNT)
    write_test(data_gen)
    read_test()
