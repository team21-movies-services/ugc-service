from time import time
from uuid import uuid4

import pytest_asyncio

from schemas.request.user_actions import Action, ActionParent, ActionType


@pytest_asyncio.fixture()
async def fake_action_film_rating() -> Action:
    rating_data = {"rate": 10, "parent_type": ActionParent.film, "parent_id": ""}
    action = Action(
        user_id=str(uuid4()),
        film_id=str(uuid4()),
        action_type=ActionType.rating,
        action_time=int(time()),
        action_data=rating_data,
    )
    return action
