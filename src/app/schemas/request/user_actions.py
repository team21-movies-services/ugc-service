from enum import IntEnum, StrEnum, auto

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field, model_validator


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


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


class ActionData(BaseModel):
    model_config = ConfigDict(extra='forbid')
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


class Action(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, json_encoders={ObjectId: str})
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    action_type: ActionType = Field(alias='actionType')
    action_time: int = Field(alias='actionTime')
    action_data: FavoriteData | CommentData | RatingData | ReactionData = Field(alias='actionData')

    @model_validator(mode='after')
    def set_action_data_type(cls, values):
        action_data = values.action_data

        # model_mapping = {
        #     ActionType.comment: CommentData,
        #     ActionType.reaction: ReactionData,
        #     ActionType.rating: RatingData,
        #     ActionType.favorite: FavoriteData
        # }
        #
        # values.action_data = model_mapping[action_type].model_validate(action_data)

        match values.action_type:
            case ActionType.reaction:
                values.action_data = ReactionData.model_validate(action_data)
            case ActionType.rating:
                values.action_data = RatingData.model_validate(action_data)
            case ActionType.favorite:
                values.action_data = FavoriteData.model_validate(action_data)
            case ActionType.comment:
                values.action_data = CommentData.model_validate(action_data)
