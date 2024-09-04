from src.users.errors.profile_error import (
    ProfileDoesNotExist,
    ProfileNotFound,
    PhoneAlreadyExists,
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
    # profile
    "ProfileDoesNotExist",
    "ProfileNotFound",
    "PhoneAlreadyExists",
]
