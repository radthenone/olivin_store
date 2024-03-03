#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv

from src.core.config import PROJECT_DIR

load_dotenv(PROJECT_DIR / '.envs' / '.env')

IS_TYPE = os.getenv("IS_TYPE", "dev")


def main():
    """Run administrative tasks."""
    if IS_TYPE == "prod":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings.prod')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
