import logging
import os
import smtplib

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
    host = settings.EMAIL_HOST
    user = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    def connect(self, **kwargs) -> smtplib.SMTP:
        try:
            if not self.client:
                client = smtplib.SMTP(self.host, self.port)
                client.starttls()
                client.login(self.user, self.password)
                self.client = client
                return self.client
        except smtplib.SMTPException as error:
            logger.error(error)

        except Exception as error:
            logger.error(error)

    def disconnect(self, **kwargs) -> None:
        self.client.quit()
