from django.db import models

from src.common.models import CreatedUpdatedDateModel
from src.orders.models.order_model import Order

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
    city = models.CharField(
        max_length=100,
    )
    street = models.CharField(
        max_length=100,
    )
    building_number = models.CharField(
        max_length=100,
    )
    postal_code = models.CharField(
        max_length=100,
    )
    country_code = models.CharField(
        max_length=100,
    )

    def __str__(self):
        return f"{self.city}, {self.street}, {self.building_number}, {self.postal_code}, {self.country_code}"
