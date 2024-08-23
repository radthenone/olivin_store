import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional

import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from ninja_extra.exceptions import APIException

from src.auth import errors as auth_errors
from src.auth.errors import (
    InvalidCredentials,
    InvalidToken,
    TokenExpired,
)

logger = logging.getLogger(__name__)


def check_passwords_match(
    password: str,
    hashed_password: str,
) -> bool:
    return check_password(password, hashed_password)


def hash_password(password: str) -> str:
    password = make_password(password)

    return password


def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()

    to_encode.update(
        {
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + expires_delta,
            "jti": str(uuid.uuid4()),
        }
    )
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_jwt_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        logger.info("Token decoded: %s", payload)
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpired
    except jwt.InvalidTokenError:
        raise InvalidToken
    except jwt.PyJWTError:
        raise InvalidCredentials
    except APIException:
        raise auth_errors.InvalidToken


def get_access_token(
    username: str,
    user_id: uuid.UUID,
    token_type: str = "access",
) -> str:
    access_token_expires = timedelta(minutes=float(settings.ACCESS_TOKEN_EXPIRE))
    access_token = create_jwt_token(
        data={
            "username": username,
            "user_id": str(user_id),
            "token_type": token_type,
        },
        expires_delta=access_token_expires,
    )
    logger.info(
        "Access token created: [green]%s[/] for [blue]%s[/] minutes",
        access_token,
        int(access_token_expires.total_seconds()) // 60,
        extra={"markup": True},
    )
    return access_token


def get_refresh_token(
    username: str,
    user_id: uuid.UUID,
    token_type: str = "refresh",
) -> str:
    refresh_token_expires = timedelta(minutes=float(settings.REFRESH_TOKEN_EXPIRE))
    refresh_token = create_jwt_token(
        data={
            "username": username,
            "user_id": str(user_id),
            "token_type": token_type,
        },
        expires_delta=refresh_token_expires,
    )
    logger.info(
        "Refresh token created: [green]%s[/] for [blue]%s[/] minutes",
        refresh_token,
        int(refresh_token_expires.total_seconds()) // 60,
        extra={"markup": True},
    )
    return refresh_token


def encode_jwt_token(username: str, user_id: uuid.UUID) -> dict:
    access_token = get_access_token(username, user_id)
    refresh_token = get_refresh_token(username, user_id)
    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
    return data


def get_backend_url(add_path: str = "") -> str:
    if settings.DJANGO_HOST == "0.0.0.0":
        host = "127.0.0.1"
        port = settings.DJANGO_PORT
        base_url = f"http://{host}:{port}"
    else:
        base_url = f"{settings.API_BACKEND_URL}"
    return f"{base_url}{add_path}"
