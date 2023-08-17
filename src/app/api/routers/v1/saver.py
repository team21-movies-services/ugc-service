import logging
from typing import Any

from fastapi import APIRouter, Depends

from dependencies.auth import get_auth_data
from schemas.domain.auth import AuthData
from schemas.request.user_actions import Action
from schemas.response.user_actions import ActionIdResponse
from services.saver import ActionSaverServiceABC

router = APIRouter(prefix='/actions', tags=['Action'])

logger = logging.getLogger().getChild('-router')


@router.post(
    '',
    summary="Сохранить действие пользователя",
    response_model=ActionIdResponse,
)
async def save_user_action(
    action: Action,
    auth_data: AuthData = Depends(get_auth_data),
    saver_service: ActionSaverServiceABC = Depends(),
) -> Any:
    result = await saver_service.save_action(action=action)
    logger.info(result)
    return result
