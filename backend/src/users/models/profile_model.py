import json
import uuid
from typing import Any, Optional

from django.conf import settings
from django.db import models
from django.utils import timezone

from src.common.mixins import ModelToDictToJsonMixin


class Profile(models.Model, ModelToDictToJsonMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    birth_date = models.DateField(
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
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    created_at = models.DateTimeField(
        db_index=True,
        default=timezone.now,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Profile of {self.user} "
