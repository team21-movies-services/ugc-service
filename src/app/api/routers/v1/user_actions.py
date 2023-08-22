import logging

from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.auth import get_auth_data
from schemas.domain.auth import AuthData
from schemas.request.user_actions import ActionCreateRequest, FilterRequest, UpdateInfo
from schemas.response.user_action import ActionIdResponse
from services.user_action import UserActionServiceABC

router = APIRouter(prefix='/actions', tags=['Action'])

logger = logging.getLogger().getChild('user-action-router')


@router.post(
    '',
    summary="Сохранить действие пользователя",
    response_model=ActionIdResponse,
    status_code=status.HTTP_201_CREATED,
)
async def save_user_action(
    action: ActionCreateRequest,
    auth_data: AuthData = Depends(get_auth_data),
    action_service: UserActionServiceABC = Depends(),
) -> ActionIdResponse:
    result = await action_service.save_action(action=action)
    return result


@router.delete('', summary="Удалить действие пользователя", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_action(
    delete_info: FilterRequest,
    action_service: UserActionServiceABC = Depends(),
    auth_data: AuthData = Depends(get_auth_data),
):
    result = await action_service.delete_action(delete_info)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action not found")


@router.patch(
    '',
    summary="Изменить действие пользователя",
    status_code=status.HTTP_200_OK,
)
async def update_user_action(
    delete_info: UpdateInfo,
    action_service: UserActionServiceABC = Depends(),
    auth_data: AuthData = Depends(get_auth_data),
) -> bool:
    result = await action_service.update_action(update_info=delete_info)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Action not found')

    return result
