from django.db import models

from src.common.models import CreatedUpdatedDateModel
from src.orders.models.order_model import Order
from src.users.models import User

# Create your models here.


class Shipping(CreatedUpdatedDateModel):
    _id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    # relationships
    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        related_name="shipping",
        null=True,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name="shipping",
        null=True,
    )
