import logging

from fastapi import APIRouter, Depends

from dependencies.auth import get_auth_data
from schemas.domain.auth import AuthData
from schemas.request.user_actions import Action
from schemas.response.user_action import ActionIdResponse
from services.user_action import UserActionServiceABC

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
    action_service: UserActionServiceABC = Depends(),
) -> ActionIdResponse:
    result = await action_service.save_action(action=action)
    return result
