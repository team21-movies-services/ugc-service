from time import time

from aiokafka import ConsumerRecord
from pydantic import BaseModel


class MovieViewed(BaseModel):
    viewed_frame: int
    film_id: str
    user_id: str

    def transform_for_clickhouse(self) -> tuple:
        return self.user_id, self.film_id, self.viewed_frame, int(time())

    @classmethod
    def from_consumer_record(cls, record: ConsumerRecord):
        key: bytes = record.key or b''
        value: bytes = record.value or b''
        user_id, film_id = key.decode().split('+')
        return cls(user_id=user_id, film_id=film_id, viewed_frame=int(value.decode()))
