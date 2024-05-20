from typing import NewType

from django.contrib.auth import get_user_model

from src.users.models import Profile

User = get_user_model()


UserType = NewType("UserType", User)
ProfileType = NewType("ProfileType", Profile)
