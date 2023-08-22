import uuid
from datetime import datetime
from typing import Generator

from schemas.request.user_actions import Action, ActionType


def gen_user_actions_data(
    action: ActionType,
    batch_size: int,
    batch_amount: int,
) -> Generator[list[Action], None, None]:
    for _ in range(batch_amount):
        user_id = uuid.uuid4()
        yield [
            Action(
                user_id=str(user_id),
                film_id=str(uuid.uuid4()),
                action_type=action,
                action_time=int(datetime.utcnow().second),
            )
            for _ in range(batch_size)
        ]
