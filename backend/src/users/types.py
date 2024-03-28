from typing import TypeVar

from django.contrib.auth.models import User

UserType = TypeVar("UserType", bound=User)
