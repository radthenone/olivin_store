from django.db import models

# Create your models here.


class Category(models.Model):
    _id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name
