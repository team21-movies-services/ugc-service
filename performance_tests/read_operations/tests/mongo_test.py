from typing import Iterable
from uuid import UUID

from config import Config
from gen_data import gen_user_actions_data
from pymongo import ASCENDING, MongoClient
from tqdm import tqdm

from schemas.request.user_actions import Action, ActionType
from utils import timer_dec

BATCH_SIZE: int = 1
BATCH_AMOUNT: int = 1

config = Config()
client: MongoClient[Action] = MongoClient("mongodb://localhost:27017/?uuidRepresentation=standard")
db = client["test-database"]
collection = db["test-collection"]


@timer_dec
def write_test(data: Iterable) -> list[UUID]:
    users = []

    collection.create_index((("user_id", ASCENDING), ("film_id", ASCENDING)), unique=True)

    for batch in tqdm(data, total=BATCH_AMOUNT):
        documents = [{"user_id": item.user_id, "film_id": item.film_id} for item in batch]
        collection.insert_many(documents)
        users.append(documents[0]["user_id"])

    return users


@timer_dec
def read_test(data: list[UUID]) -> None:
    for user_id in tqdm(data, total=len(data)):
        tuple(collection.find({"user_id": user_id}))


if __name__ == '__main__':
    action_batch = gen_user_actions_data(action=ActionType.favorite, batch_size=BATCH_SIZE, batch_amount=BATCH_AMOUNT)
    read_test(write_test(action_batch))
