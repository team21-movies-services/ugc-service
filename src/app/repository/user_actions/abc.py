from abc import ABC, abstractmethod

from schemas.request.user_actions import Action


class AbstractUserActionRepository(ABC):
    @abstractmethod
    async def insert_action(self, action: Action):
        """Метод для сохранения действий пользователя в mongodb"""
        pass
