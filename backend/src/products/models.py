from django.db import models

from src.categories.models import Category
from src.common.models import CreatedUpdatedDateModel
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

    def __str__(self):
        return self.name
