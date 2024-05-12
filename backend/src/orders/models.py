import enum

from django.db import models

from src.common.models import CreatedUpdatedDateModel
from src.users.models import User

# Create your models here.


class OrderStatus(enum.Enum):
    CREATED = "CREATED"
    ORDERED = "ORDERED"
    PREPARED = "PREPARED"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"
    DELIVERED = "DELIVERED"
    RETURNED = "RETURNED"
    DELETED = "DELETED"


class PaymentMethod(enum.Enum):
    pass


class Order(CreatedUpdatedDateModel):
    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    payment_method = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    tax_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    shipping_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    return_relation = models.TextField(
        null=True,
        blank=True,
    )
    return_is_approved = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )
    return_timeleft = models.IntegerField(
        default=14,
        null=True,
        blank=True,
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    return_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=100,
        choices=[(s.name, s.value) for s in OrderStatus],
        default=OrderStatus.CREATED.value,
    )
    # relationships
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
    )
