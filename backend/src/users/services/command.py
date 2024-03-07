import argparse
import os

import django
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings.base")
django.setup()

User = get_user_model()

parser = argparse.ArgumentParser(
    description="Create a superuser with email and password only"
)
parser.add_argument("--email", required=True, help="Superuser email")
parser.add_argument("--password", required=True, help="Superuser password")

args = parser.parse_args()


def create_superuser() -> None:
    email = args.email
    password = args.password

    try:
        User.objects.get(email=email)
        print(f"User with email {email} already exists.")
    except ObjectDoesNotExist:
        user = User(email=email, password=password, is_staff=True, is_superuser=True)
        user.set_password(password)
        user.save()
        print("Superuser created successfully.")


create_superuser()
