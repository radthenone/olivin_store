from typing import TypeVar

from django.contrib.auth import get_user_model

from src.users.models import Profile

User = get_user_model()

UserType = TypeVar("UserType", bound=User)
ProfileType = TypeVar("ProfileType", bound=Profile)
