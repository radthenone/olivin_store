from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from src.users.models import User

UserType = TypeVar("UserType", bound=User)
