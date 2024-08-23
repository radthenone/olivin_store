import logging
from typing import Optional

from django.conf import settings

from src.data.interfaces import IRegistrationEmailHandler
from src.data.managers.mail_manager import MailManager

logger = logging.getLogger(__name__)


class RegistrationEmailHandler(IRegistrationEmailHandler):
    def __init__(self, manager: MailManager):
        self.manager = manager

    def send_registration_email(
        self,
        to_email: str,
        subject: str = "Welcome to our platform!",
        template_name: str = "register-mail",
        from_email: Optional[str] = settings.EMAIL_HOST_USER,
        context: Optional[dict] = None,
    ) -> bool:
        to_email = [to_email]
        return self.manager.send_mail(
            subject=subject,
            template_name=template_name,
            context=context,
            to_email=to_email,
            from_email=from_email,
            files=None,
            fail_silently=False,
        )
