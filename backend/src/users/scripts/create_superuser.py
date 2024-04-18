import argparse
import logging
import os
import warnings

import django
from django.core.exceptions import ObjectDoesNotExist

from src.users.repositories import UserRepository
from src.users.schemas.user_schema import SuperUserCreateSchema
from src.users.services import UserService

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.base"),
)

warnings.filterwarnings("ignore", message=".*'src.users.commands.create_superuser'.*")
django.setup()


user_service = UserService(repository=UserRepository())

logger = logging.getLogger(__name__)


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
        user_super_create = SuperUserCreateSchema(
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user_service.create_superuser(
            user_super_create=user_super_create,
        )
        logger.info("Superuser created successfully with email %s", email)
    except ObjectDoesNotExist:
        logger.error("Superuser with email %s already exists", email)


if __name__ == "__main__":
    create_superuser()
