from django.db import models

from src.common.models import CreatedUpdatedDateModel
from src.users.models.user_model import User


class Profile(CreatedUpdatedDateModel):
    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    avatar = models.URLField(
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=12,
        null=True,
        blank=True,
    )
    # relationships
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    def __str__(self):
        return f"Profile of {self.user.email}"
