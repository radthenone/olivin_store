from typing import Optional

from django.contrib.auth.hashers import check_password

from src.users.errors import NotAuthenticated, UserNotFound
from src.users.types import UserType


class UserService:
    def __init__(self, repository, *args, **kwargs):
        self.user_repository = repository
        super().__init__(*args, **kwargs)

    def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> Optional["UserType"]:
        user = self.user_repository.get_user_by_username(username)
        if user is None:
            raise UserNotFound
        if not check_password(password, user.password):
            raise NotAuthenticated
        return user
