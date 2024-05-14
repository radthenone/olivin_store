from django.db import models

from src.common.models import CreatedUpdatedDateModel

# Create your models here.


class Address(CreatedUpdatedDateModel):
    id = models.AutoField(
        primary_key=True,
        editable=False,
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
