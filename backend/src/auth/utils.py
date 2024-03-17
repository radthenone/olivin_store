import logging
import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password

from src.auth.errors import InvalidCredentials, InvalidToken, TokenExpired

logger = logging.getLogger(__name__)


def check_passwords_match(
    password: str,
    hashed_password: str,
) -> bool:
    return check_password(password, hashed_password)


def hash_password(password: str) -> str:
    password = make_password(password)

    return password


def create_jwt_token(data: dict, expires_delta: timedelta) -> dict:
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
    logger.info("Token created: %s", encoded_jwt)
    return encoded_jwt


def decode_jwt_token(token: str) -> dict:
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


def get_access_token(
    username: str,
    user_id: uuid.UUID,
    token_type: str = "access",
) -> dict:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(
        data={
            "username": username,
            "user_id": str(user_id),
            "token_type": token_type,
        },
        expires_delta=access_token_expires,
    )
    logger.info("Access token created: %s", access_token)
    return access_token


def get_refresh_token(
    username: str,
    user_id: uuid.UUID,
    token_type: str = "refresh",
) -> dict:
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_jwt_token(
        data={
            "username": username,
            "user_id": str(user_id),
            "token_type": token_type,
        },
        expires_delta=refresh_token_expires,
    )
    logger.info("Refresh token created: %s", refresh_token)
    return refresh_token


def encode_jwt_token(username: str, user_id: uuid.UUID) -> dict:
    access_token = get_access_token(username, user_id)
    refresh_token = get_refresh_token(username, user_id)
    data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
    logger.info("Tokens set: %s", data)
    return data
