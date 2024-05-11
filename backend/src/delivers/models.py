from django.db import models

from src.common.models import CreatedUpdatedDateModel

# Create your models here.


class Deliver(CreatedUpdatedDateModel):
    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    address = models.TextField(
        null=True,
        blank=True,
    )
    is_delivered = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )
    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )
