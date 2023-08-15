from datetime import datetime

from pydantic import UUID4, BaseModel


class FavoriteMovie(BaseModel):
    movie_id: UUID4
    created_at: datetime
