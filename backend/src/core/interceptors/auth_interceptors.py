import logging
from typing import Optional
from uuid import UUID

from ninja.security import HttpBearer

from src.auth.utils import decode_jwt_token, get_token_from_request
from src.common.utils import Depends

logger = logging.getLogger(__name__)


def verify_jwt(
    get_token: str = Depends(get_token_from_request),
) -> bool:
    token = decode_jwt_token(token=get_token)
    if token:
        return True
    return False


def get_user_id(
    get_token: str = Depends(get_token_from_request),
) -> Optional[UUID]:
    token = decode_jwt_token(token=get_token)
    if token:
        user_id = token.get("user_id")
        return user_id
    return None


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        token = decode_jwt_token(token=token)
        if token:
            return token
        return None
