import logging
import os
import smtplib
from typing import Optional

from django.conf import settings

from src.data.interfaces.client.abstract_client import IClient

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "src.core.settings.dev"),
)


logger = logging.getLogger(__name__)


class MailClient(IClient):
    client: smtplib.SMTP = None
    port = settings.EMAIL_PORT
    host = settings.EMAIL_HOST if settings.EMAIL_HOST != "127.0.0.1" else "localhost"
    user = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    def connect(self, retries=3, **kwargs) -> Optional[smtplib.SMTP]:
        attempt = 0
        while attempt < retries:
            try:
                client = smtplib.SMTP(self.host, self.port)
                if self.user and self.password:
                    client.login(self.user, self.password)
                self.client = client
                logger.info("Successfully connected to the SMTP server")
                return self.client
            except smtplib.SMTPException as error:
                attempt += 1
                logger.error(
                    f"Attempt {attempt} - Failed to connect to SMTP server: {str(error)}"
                )
                if attempt == retries:
                    return None
        return None

    def disconnect(self, **kwargs) -> None:
        if self.client:
            try:
                self.client.quit()
                logger.info("Successfully disconnected from the SMTP server")
            except smtplib.SMTPException as error:
                logger.error(f"Failed to disconnect from the SMTP server: {str(error)}")
            finally:
                self.client = None
