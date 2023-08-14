from enum import IntEnum, StrEnum, auto

from pydantic import BaseModel, ConfigDict, Field, field_validator

from schemas.utils import PyObjectId


class ActionType(StrEnum):
    comment = auto()
    favorite = auto()
    rating = auto()
    reaction = auto()


class ActionParent(StrEnum):
    film = auto()
    comment = auto()


class ReactionType(IntEnum):
    like = 1
    dislike = -1


class MongoSchema(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='forbid',
    )


class ActionData(MongoSchema):
    user_id: str
    film_id: str


class ReactionData(ActionData):
    parent_type: ActionParent
    parent_id: str
    reaction: ReactionType


class RatingData(ActionData):
    parent_type: ActionParent
    parent_id: str
    rate: int = Field(ge=1, le=10)


class FavoriteData(ActionData):
    pass


class CommentData(ActionData):
    parent_type: ActionParent
    parent_id: str
    text: str


class Action(MongoSchema):
    id: PyObjectId | None = Field(default=None, alias='_id')
    action_type: ActionType
    action_time: int
    action_data: FavoriteData | CommentData | RatingData | ReactionData

    @field_validator('action_data', mode='before')
    def set_action_data_type(cls, action_data, values):
        match values.data.get('action_type'):
            case ActionType.reaction:
                action_data = ReactionData(**action_data)
            case ActionType.rating:
                action_data = RatingData(**action_data)
            case ActionType.favorite:
                action_data = FavoriteData(**action_data)
            case ActionType.comment:
                action_data = CommentData(**action_data)

        return action_data
