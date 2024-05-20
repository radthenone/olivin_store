from django.core.management.base import BaseCommand, CommandError

from src.users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--email", required=True, help="Superuser email")
        parser.add_argument("--password", required=True, help="Superuser password")

    def handle(self, *args, **options):
        email = options["email"]
        password = options["password"]

        if User.objects.filter(email=email).exists():
            raise CommandError(f"Superuser with email {email} already exists")

        try:
            user_db = User(
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True,
            )
            user_db.set_password(user_db.password)
            user_db.save()

            self.stdout.write(
                self.style.SUCCESS(f"Superuser created with email {email}")
            )
        except Exception as error:
            raise CommandError(f"Error while creating superuser: {error}")
