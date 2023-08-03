from pydantic import UUID4, BaseModel


class SaveViewDataResponse(BaseModel):
    message: str
    user_id: UUID4
    movie_id: UUID4
    viewed_frame: int
