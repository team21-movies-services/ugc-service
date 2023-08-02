from pydantic import BaseModel, UUID4


class SaveViewDataResponse(BaseModel):
    message: str
    user_id: UUID4
    movie_id: UUID4
    viewed_frame: int
