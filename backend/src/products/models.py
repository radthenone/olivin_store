from django.db import models

from src.categories.models import Category
from src.common.models import CreatedUpdatedDateModel
from src.events.models import Event
from src.users.models import User

# Create your models here.


class Product(CreatedUpdatedDateModel):
    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    image = models.URLField()
    brand = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    event_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    rating = (
        models.DecimalField(
            max_digits=7,
            decimal_places=2,
            null=True,
            blank=True,
        ),
    )
    num_reviews = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    count_in_stock = models.IntegerField(
        default=0,
        null=True,
        blank=True,
    )
    is_event = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    # relationships
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=False,
        related_name="products",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
    )
    events = models.ManyToManyField(
        Event,
        through="ProductEvent",
        through_fields=("product", "event"),
    )

    def __str__(self):
        return self.name


class ProductEvent(models.Model):
    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    event_product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
