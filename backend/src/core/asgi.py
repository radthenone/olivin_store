"""
ASGI config for core_old project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

from src.core.config import PROJECT_DIR

load_dotenv(PROJECT_DIR / '.envs' / '.env')

IS_TYPE = os.getenv("IS_TYPE", "dev")

if IS_TYPE == "prod":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings.dev')

application = get_asgi_application()