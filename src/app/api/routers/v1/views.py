import logging

from dependencies.auth import get_auth_data
from fastapi import APIRouter, Depends, Query
from pydantic import UUID4
from schemas.domain.auth import AuthData
from services.views import ViewsServiceABC
from schemas.response.views import SaveViewDataResponse

router = APIRouter(prefix='/views', tags=['Views'])

logger = logging.getLogger().getChild('views-router')


@router.post(
    '/{movie_id}',
    summary="Сохранить данные о просмотре",
    response_model=SaveViewDataResponse,
)
async def save_movie_view(movie_id: UUID4,
                          auth_data: AuthData = Depends(get_auth_data),
                          viewed_frame: int = Query(None, description="Просмотренная секунда фильма"),
                          view_service: ViewsServiceABC = Depends()) -> SaveViewDataResponse:

    movie_view_data = await view_service.save_view_data(
        movie_id=movie_id,
        user_id=auth_data.user_id,
        viewed_frame=viewed_frame)

    return movie_view_data
