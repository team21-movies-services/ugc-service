from pydantic import BaseModel


class FilmRating(BaseModel):
    count_likes: int
    count_dislikes: int
    average_rating: float
