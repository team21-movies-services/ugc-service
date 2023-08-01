from pydantic import BaseModel


class MovieViewed(BaseModel):
    viewed_frame: int
    film_id: str
    user_id: str
