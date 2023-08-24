from time import time
from uuid import uuid4

import pytest_asyncio

from schemas.request.user_actions import ActionCreateRequest, ActionParent, ActionType


@pytest_asyncio.fixture()
def make_review_pack() -> list[dict]:
    result = []
    for _ in range(25):
        result.append(
            ActionCreateRequest(
                user_id=str(uuid4()),
                action_type=ActionType.comment,
                film_id='998ba1aa-725d-4db3-b928-a5d6fad38fb3',
                action_time=int(time()),
                action_data=dict(
                    parent_type=ActionParent.film,
                    parent_id='998ba1aa-725d-4db3-b928-a5d6fad38fb3',
                    text='Some random text',
                ),
            )
        )
    return [action.model_dump() for action in result]
