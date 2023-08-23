from time import time

import pytest_asyncio


@pytest_asyncio.fixture()
async def make_comment() -> dict:
    comment = {
        "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
        "film_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
        "action_type": "comment",
        "action_time": time(),
        "action_data": {"parent_type": "film", "parent_id": "64e3676cec293c29b50d38fc", "text": "Some comment text"},
    }
    return comment


@pytest_asyncio.fixture()
async def make_reaction() -> dict:
    reaction = {
        "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
        "film_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
        "action_type": "reaction",
        "action_time": time(),
        "action_data": {"parent_type": "film", "parent_id": "64e3676cec293c29b50d38fc", "reaction": 1},
    }
    return reaction


@pytest_asyncio.fixture()
async def make_favorite() -> dict:
    favorite = {
        "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
        "film_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
        "action_type": "favorite",
        "action_time": time(),
    }
    return favorite


@pytest_asyncio.fixture()
async def make_rating() -> dict:
    rating = {
        "user_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
        "film_id": "4bc7233d-c87e-4b6a-afc2-d025ecdf2397",
        "action_type": "rating",
        "action_time": time(),
        "action_data": {"parent_type": "film", "parent_id": "64e3676cec293c29b50d38fc", "rate": 0},
    }
    return rating
