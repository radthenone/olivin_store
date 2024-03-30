from typing import TypeVar

from django.contrib.auth import get_user_model

User = get_user_model()

UserType = TypeVar("UserType", bound=User)
