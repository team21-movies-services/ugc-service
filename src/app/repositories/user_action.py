import logging
from abc import ABC, abstractmethod
from typing import assert_never

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pymongo.errors import PyMongoError
from pymongo.results import DeleteResult, InsertOneResult, UpdateResult

from core.config import Settings
from schemas.request.user_actions import (
    Action,
    ActionCreateRequest,
    CommentFilterRequest,
    CommentUpdateRequest,
    FavoriteFilterRequest,
    FilterRequest,
    RatingFilterRequest,
    RatingUpdateRequest,
    ReactionFilterRequest,
    ReactionUpdateRequest,
    UpdateInfo,
)

logger = logging.getLogger().getChild('user-action-repository')


class UserActionRepository(ABC):
    @abstractmethod
    async def insert_action(self, action: Action) -> str | None:
        """
        Вставляет данные о действии пользователя в базу данных.

        Args:
            action (ActionCreateRequest): Объект, содержащий информацию о действии пользователя.

        Returns:
            str: Возвращает идентификатор вставленной записи.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_action(self, update_info: UpdateInfo) -> bool:
        """
        Обновляет информации о действии пользователя в базе данных.

        Args:
            update_info (UpdateInfo): Объект, содержащий информацию об обновлении действия.

        Returns:
            bool: Возвращает True, если запись была обновлена, иначе False.
        Raises:
            TypeError: Если тип `update_info` не соответствует ожидаемым типам (CommentUpdateRequest,
                ReactionUpdateRequest или RatingUpdateRequest).
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_action(self, delete_info: FilterRequest) -> bool:
        """
        Удаляет действие пользователя из базы данных в соответствии с переданным фильтром.

        Args:
            delete_info (FilterRequest): Объект, содержащий информацию для поиска действия.

        Returns:
            bool: Возвращает True, если действие было удалено, иначе False.
        """
        raise NotImplementedError


class MongoUserActionRepository(UserActionRepository):
    def __init__(self, client: AsyncIOMotorClient, settings: Settings):
        self.client = client
        self.db: AsyncIOMotorDatabase = self.client[settings.mongo.database]
        self.collection: AsyncIOMotorCollection = self.db[settings.mongo.collection]

    async def insert_action(self, action: ActionCreateRequest) -> str | None:
        insert_data = action.model_dump(by_alias=True, exclude_none=True)
        try:
            result: InsertOneResult = await self.collection.insert_one(insert_data)
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error("Error occurred during insert operation: {}".format(str(e)))
        return None

    async def delete_action(self, delete_info: FilterRequest) -> bool:
        _filter = {"action_type": delete_info.action_type}
        match delete_info:
            case CommentFilterRequest():  # type: ignore[misc]
                _filter.update({"_id": delete_info.id})
            case ReactionFilterRequest():  # type: ignore[misc]
                _filter.update({"user_id": delete_info.user_id, "action_data.parent_id": str(delete_info.parent_id)})
            case RatingFilterRequest():  # type: ignore[misc]
                _filter.update({"user_id": delete_info.user_id, "action_data.parent_id": str(delete_info.parent_id)})
            case FavoriteFilterRequest():  # type: ignore[misc]
                _filter.update(delete_info.model_dump(by_alias=True))
            case _ as unreachable:
                assert_never(unreachable)
        logger.info("Deleting action with query: {}".format(_filter))
        try:
            result: DeleteResult = await self.collection.delete_one(_filter)
            if result.deleted_count == 1:
                logger.info("Deleted action with query {}".format(_filter))
                return True
        except PyMongoError as e:
            logger.error("Error occurred during delete operation: {}".format(str(e)))
        return False

    async def update_action(self, update_info: UpdateInfo) -> bool:
        match update_info:
            case CommentUpdateRequest():  # type: ignore[misc]
                _filter = {"_id": update_info.id, "action_type": update_info.action_type}
                new_value = {"action_data.text": update_info.text}
            case ReactionUpdateRequest():  # type: ignore[misc]
                _filter = {
                    "action_type": update_info.action_type,
                    "user_id": update_info.user_id,
                    "action_data.parent_id": str(update_info.parent_id),
                }
                new_value = {"action_data.reaction": update_info.reaction}
            case RatingUpdateRequest():  # type: ignore[misc]
                _filter = {
                    "action_type": update_info.action_type,
                    "user_id": update_info.user_id,
                    "action_data.parent_id": str(update_info.parent_id),
                }
                new_value = {"action_data.rate": update_info.rate}
            case _ as unreachable:
                assert_never(unreachable)

        logger.info("Updating action with filter {0} and set {1}".format(_filter, new_value))
        try:
            result: UpdateResult = await self.collection.update_one(filter=_filter, update={"$set": new_value})
            if result.matched_count == 1:
                logger.info("One match with filter {0}")
            if result.modified_count == 1:
                logger.info("Updated action with filter {0} and set {1}".format(_filter, new_value))
                return True

        except PyMongoError as e:
            logger.error("Error occurred during update operation: {}".format(str(e)))
        return False
