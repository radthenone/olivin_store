from django.db import models

from src.common.models import CreatedUpdatedDateModel
from src.products.models import Product
from src.users.models import User

# Create your models here.


class Review(CreatedUpdatedDateModel):
    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    rating = models.ImageField(
        default=0,
        null=True,
        blank=True,
    )
    comment = models.TextField(
        null=True,
        blank=True,
    )
    # relationships
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name="reviews",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="reviews",
    )

    def __str__(self):
        return self.name
