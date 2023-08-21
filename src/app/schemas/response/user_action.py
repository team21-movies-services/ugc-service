from pydantic import UUID4, BaseModel


class ActionIdResponse(BaseModel):
    action_id: str
    user_id: UUID4
