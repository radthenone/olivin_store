from src.users.errors.profile_error import (
    PhoneAlreadyExists,
    ProfileDoesNotExist,
    ProfileNotFound,
)
from src.users.errors.user_error import (
    EmailAlreadyExists,
    EmailAlreadyInUse,
    EmailDoesNotExist,
    EmailUpdateFailed,
    SuperUserCreateFailed,
    UserCreateFailed,
    UserDoesNotExist,
    UsernameAlreadyExists,
    UserNotFound,
    UserUpdateFailed,
    WrongOldEmail,
    WrongPassword,
)

__all__ = [
    # user
    "UsernameAlreadyExists",
    "EmailAlreadyExists",
    "UserDoesNotExist",
    "WrongPassword",
    "UserNotFound",
    "EmailDoesNotExist",
    "UserCreateFailed",
    "SuperUserCreateFailed",
    "EmailAlreadyInUse",
    "WrongOldEmail",
    "EmailUpdateFailed",
    "UserUpdateFailed",
    # profile
    "ProfileDoesNotExist",
    "ProfileNotFound",
    "PhoneAlreadyExists",
]
