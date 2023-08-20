from pydantic import UUID4, BaseModel

from schemas.utils import PyObjectId


class ActionIdResponse(BaseModel):
    action_id: PyObjectId
    user_id: UUID4
