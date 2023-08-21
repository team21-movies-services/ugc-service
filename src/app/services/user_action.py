import logging
from abc import ABC, abstractmethod

from repositories.user_action import MongoUserActionRepository
from schemas.request.user_actions import ActionCreateRequest, FilterRequest, UpdateInfo
from schemas.response.user_action import ActionIdResponse

logger = logging.getLogger().getChild('user_action-service')


class UserActionServiceABC(ABC):
    @abstractmethod
    async def save_action(self, action: ActionCreateRequest) -> ActionIdResponse:
        """Сохранить действие в хранилище"""
        raise NotImplementedError

    @abstractmethod
    async def delete_action(self, delete_info) -> int:
        """Удалить действие из хранилища"""

    @abstractmethod
    async def update_action(self, update_info):
        """Изменить действие"""


class UserActionService(UserActionServiceABC):
    def __init__(self, user_action_repository: MongoUserActionRepository):
        self._user_action_repository = user_action_repository

    async def save_action(self, action: ActionCreateRequest) -> ActionIdResponse:
        result = await self._user_action_repository.insert_action(action)
        return ActionIdResponse(action_id=result, user_id=action.user_id)

    async def delete_action(self, delete_info: FilterRequest) -> bool:
        result = await self._user_action_repository.delete_action(delete_info)
        return result

    async def update_action(self, update_info: UpdateInfo) -> bool:
        result = await self._user_action_repository.update_action(update_info)
        return result
