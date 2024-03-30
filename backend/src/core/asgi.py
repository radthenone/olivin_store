"""
ASGI config for core_old project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import warnings

from django.core.asgi import get_asgi_application

warnings.filterwarnings(
    "ignore", message="StreamingHttpResponse must consume synchronous iterators"
)
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


application = get_asgi_application()
