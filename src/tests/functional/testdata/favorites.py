from time import time
from uuid import uuid4

import pytest_asyncio

from schemas.domain.auth import AuthData
from schemas.request.user_actions import ActionCreateRequest, ActionType


@pytest_asyncio.fixture()
async def make_my_favorite(auth_user: AuthData) -> dict:
    return ActionCreateRequest(
        user_id=str(auth_user.user_id),
        film_id=str(uuid4()),
        action_type=ActionType.favorite,
        action_time=int(time()),
    ).model_dump()
