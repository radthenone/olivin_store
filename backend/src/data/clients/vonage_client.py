import logging
import os
from typing import Optional

from django.conf import settings
from vonage.client import Client

from src.data.interfaces.client.abstract_client import IClient

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)

logger = logging.getLogger(__name__)


class VonageClient(IClient):
    client: Optional[Client] = None

    def connect(
        self,
        api_key: str = settings.VONAGE_API_KEY,
        api_secret: str = settings.VONAGE_API_SECRET,
    ) -> Optional[Client]:
        try:
            client = Client(
                key=settings.VONAGE_API_KEY,
                secret=settings.VONAGE_API_SECRET,
            )
            return client
        except Exception as e:
            logger.exception("connect: %s", e)
            return None

    def disconnect(self) -> None:
        self.client = None
