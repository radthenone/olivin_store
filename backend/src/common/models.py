import json
import uuid
from typing import Any, Optional

from django.db import models
from django.utils import timezone


class CreatedUpdatedDateModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
