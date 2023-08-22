from enum import IntEnum, StrEnum, auto
from typing import Literal, Union

from pydantic import UUID4, BaseModel, ConfigDict, Field, field_validator

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
    parent_type: ActionParent
    parent_id: UUID4 | PyObjectId


class ReactionData(ActionData):
    reaction: ReactionType


class RatingData(ActionData):
    rate: int = Field(ge=0, le=10)


class CommentData(ActionData):
    text: str


class Action(MongoSchema):
    id: PyObjectId | None = Field(default=None, alias='_id')
    user_id: UUID4
    film_id: UUID4
    action_type: ActionType
    action_time: int
    action_data: CommentData | RatingData | ReactionData | None = Field(default=None)

    @field_validator('action_data', mode='before')
    def set_action_data_type(cls, action_data, values):
        match values.data.get('action_type'):
            case ActionType.reaction:
                action_data = ReactionData(**action_data)
            case ActionType.rating:
                action_data = RatingData(**action_data)
            case ActionType.comment:
                action_data = CommentData(**action_data)

        return action_data


class ActionCreateRequest(MongoSchema):
    user_id: UUID4
    film_id: UUID4
    action_type: ActionType
    action_time: int
    action_data: CommentData | RatingData | ReactionData | None = Field(default=None)

    @field_validator('action_data', mode='before')
    def set_action_data_type(cls, action_data, values):
        match values.data.get('action_type'):
            case ActionType.reaction:
                action_data = ReactionData(**action_data)
            case ActionType.rating:
                action_data = RatingData(**action_data)
            case ActionType.comment:
                action_data = CommentData(**action_data)

        return action_data


class CommentFilterRequest(MongoSchema):
    action_type: Literal[ActionType.comment]
    id: PyObjectId = Field(alias="_id")


class FavoriteFilterRequest(MongoSchema):
    action_type: Literal[ActionType.favorite]
    user_id: UUID4
    film_id: UUID4


class ReactionFilterRequest(MongoSchema):
    action_type: Literal[ActionType.reaction]
    user_id: UUID4
    parent_id: PyObjectId | UUID4 = Field(alias="action_data.parent_id")


class RatingFilterRequest(MongoSchema):
    action_type: Literal[ActionType.rating]
    user_id: UUID4
    parent_id: PyObjectId | UUID4 = Field(alias="action_data.parent_id")


FilterRequest = Union[CommentFilterRequest, FavoriteFilterRequest, ReactionFilterRequest, RatingFilterRequest]


class CommentUpdateRequest(CommentFilterRequest):
    text: str = Field(alias="action_data.text")


class ReactionUpdateRequest(ReactionFilterRequest):
    reaction: ReactionType = Field(alias="action_data.reaction")


class RatingUpdateRequest(RatingFilterRequest):
    rate: int = Field(ge=0, le=10, alias="action_data.rate")


UpdateInfo = Union[RatingUpdateRequest, CommentUpdateRequest, ReactionUpdateRequest]
