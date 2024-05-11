from django.db import models

from src.common.models import CreatedUpdatedDateModel
from src.delivers.models import Deliver
from src.users.models import User

# Create your models here.


class OrderReturn(CreatedUpdatedDateModel):
    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    reason = models.TextField(
        null=True,
        blank=True,
    )
    is_returned = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )


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

    is_paid = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )
    is_received = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )
    # relationships
    order_return = models.OneToOneField(
        OrderReturn,
        on_delete=models.SET_NULL,
        related_name="order",
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
    )
    deliver = models.ForeignKey(
        Deliver,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
    )
