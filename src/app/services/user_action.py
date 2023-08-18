from abc import ABC, abstractmethod

from repositories.user_action import MongoUserActionRepository
from schemas.request.user_actions import Action
from schemas.response.user_action import ActionIdResponse


class UserActionServiceABC(ABC):
    @abstractmethod
    async def save_action(self, action: Action) -> ActionIdResponse:
        """Сохранить действие в хранилище"""
        raise NotImplementedError


class UserActionService(UserActionServiceABC):
    def __init__(self, saver_repository: MongoUserActionRepository):
        self._saver_repository = saver_repository

    async def save_action(self, action: Action) -> ActionIdResponse:
        result = await self._saver_repository.insert_action(action)
        return ActionIdResponse(action_id=result.inserted_id, user_id=action.user_id)
