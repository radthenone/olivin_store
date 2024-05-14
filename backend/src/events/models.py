from datetime import datetime

from django.db import models

# Create your models here.


class Event(models.Model):
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
    start_date = models.DateField(
        null=True,
        blank=True,
    )
    end_date = models.DateField(
        null=True,
        blank=True,
    )

    def is_active(self):
        now = datetime.now().date()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"Event: {self.name}"
