"""
WSGI config for olivin_store project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from src.core.config import PROJECT_DIR
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

load_dotenv(PROJECT_DIR / '.envs' / '.env')

IS_TYPE = os.getenv("IS_TYPE", "dev")

if IS_TYPE == "prod":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.core.settings.dev')

application = get_wsgi_application()
