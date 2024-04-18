import logging
import os

from django.conf import settings

from src.core.config import BASE_DIR

logger = logging.getLogger(__name__)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


class ApiExtra:
    VERSION: str

    def __init__(self):
        self.VERSION = self._create_version()
        self.PREFIX = self._create_prefix()
        self._connect_url()

    @staticmethod
    def _connect_url():
        django_host = settings.DJANGO_HOST
        django_port = settings.DJANGO_PORT
        if django_host == "0.0.0.0":
            django_host = "localhost"
        logger.info("http://%s:%s", django_host, django_port)

    def _create_prefix(self):
        prefix = "v"
        if self.VERSION:
            version_parts = self.VERSION.split(".")
            for i in version_parts:
                if int(i) != 0:
                    prefix += str(i)
        else:
            prefix = "v1"
        return prefix

    @staticmethod
    def _create_version():
        try:
            with open(BASE_DIR / "VERSION.txt", "r") as version_file:
                version = version_file.read()
                return version.strip()
        except FileNotFoundError:
            with open(BASE_DIR / "VERSION.txt", "w") as version_file:
                version_file.write("0.1.0")
            return "0.1.0"
