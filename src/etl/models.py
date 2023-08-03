from time import time

from pydantic import BaseModel


class MovieViewed(BaseModel):
    viewed_frame: int
    film_id: str
    user_id: str

    def transform_for_clickhouse(self) -> tuple:
        return (self.user_id, self.film_id, self.viewed_frame, int(time()))
