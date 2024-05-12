from django.db import models

# Create your models here.


class Event(models.Model):
    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )
    start_date = models.DateField(
        null=True,
        blank=True,
    )
    end_date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
