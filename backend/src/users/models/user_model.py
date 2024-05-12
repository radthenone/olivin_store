import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

from src.common.models import CreatedUpdatedDateModel

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


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


class Profile(CreatedUpdatedDateModel):
    id = models.AutoField(
        primary_key=True,
        editable=False,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        upload_to="avatars",
        null=True,
        blank=True,
    )
    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    # relationships
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="profile",
    )
