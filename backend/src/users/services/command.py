import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from dotenv import load_dotenv

from src.core.config import PROJECT_DIR

load_dotenv(PROJECT_DIR / ".envs" / ".env")

IS_TYPE = os.getenv("IS_TYPE", "dev")

if IS_TYPE == "prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings.dev")

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser with email and password only"

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True, help="Superuser email")
        parser.add_argument("--password", required=True, help="Superuser password")

    def handle(self, *args, **kwargs):
        email = kwargs["email"]
        password = kwargs["password"]

        try:
            User.objects.get(email=email)
            self.stdout.write(
                self.style.ERROR(f'User with email "{email}" already exists.')
            )
        except ObjectDoesNotExist:
            User.objects.create_superuser(
                email=email, password=password, is_staff=True, is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
