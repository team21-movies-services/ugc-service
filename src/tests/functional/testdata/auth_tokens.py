from datetime import datetime, timedelta

import jwt
import pytest_asyncio
from functional.settings import Settings

from schemas.domain.auth import AuthData


@pytest_asyncio.fixture()
async def get_access_token(auth_user: AuthData, settings: Settings) -> str:
    payload = {
        'sub': 'authentication',
        'exp': (datetime.now() + timedelta(days=1)).timestamp(),
        'iat': int(datetime.utcnow().timestamp()),
        'user_id': str(auth_user.user_id),
        'is_superuser': str(False),
    }

    return jwt.encode(payload, settings.project.jwt_secret_key, algorithm="HS256")


@pytest_asyncio.fixture()
async def get_forbidden_token(auth_user: AuthData) -> str:
    payload = {
        'sub': 'authentication',
        'exp': (datetime.now() + timedelta(days=1)).timestamp(),
        'iat': int(datetime.utcnow().timestamp()),
        'user_id': str(auth_user.user_id),
        'is_superuser': str(False),
    }

    return jwt.encode(payload, "123", algorithm="HS256")


@pytest_asyncio.fixture()
async def get_expire_token(auth_user: AuthData, settings: Settings) -> str:
    payload = {
        'sub': 'authentication',
        'exp': (datetime.now() - timedelta(days=1)).timestamp(),
        'iat': int(datetime.utcnow().timestamp()),
        'user_id': str(auth_user.user_id),
        'is_superuser': str(False),
    }

    return jwt.encode(payload, settings.project.jwt_secret_key, algorithm="HS256")
