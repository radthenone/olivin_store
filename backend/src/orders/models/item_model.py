from django.db import models

from src.common.models import CreatedUpdatedDateModel
from src.orders.models.order_model import Order
from src.products.models import Product

# Create your models here.


class OrderItem(CreatedUpdatedDateModel):
    _id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="order_items",
        null=True,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        related_name="order_items",
        null=True,
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    qty = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
