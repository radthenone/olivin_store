import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from django.conf import settings

from src.data.clients import MailClient
from src.data.tasks import attach_files_task, render_html_task

logger = logging.getLogger(__name__)


class MailManager:
    def __init__(self, client: MailClient = MailClient()):
        self.client = client
        self.smtp = self.client.connect()

    @staticmethod
    def _render_html(template_name: str, context: Optional[dict]) -> dict:
        return render_html_task.get_result(template_name, context)

    @staticmethod
    def _attach_files(msg_as_str: str, files: List[str]) -> str:
        return attach_files_task.get_result(msg_as_str, files)

    def send_mail(
        self,
        subject: str,
        to_email: List[str],
        template_name: str,
        context: Optional[dict] = None,
        from_email: str = settings.EMAIL_HOST_USER,
        files: Optional[List[str]] = None,
        fail_silently: bool = False,
    ) -> bool:
        try:
            render_result = self._render_html(template_name, context)
            html_type = render_result["html_type"]
            html_content = render_result["html_content"]

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = from_email
            msg["To"] = ", ".join(to_email)
            msg.attach(MIMEText(html_content, _subtype=html_type))

            if files:
                msg_as_str = msg.as_string()
                msg_as_str = self._attach_files(msg_as_str, files)
                msg = MIMEMultipart("alternative")
                msg.attach(MIMEText(msg_as_str, _subtype="html"))

            self.smtp.sendmail(from_email, to_email, msg.as_string())
            logger.info("Successfully sent email")
            return True
        except smtplib.SMTPException as error:
            logger.error(f"Failed to send email: {str(error)}")
            if not fail_silently:
                raise
            return False
        finally:
            self.client.disconnect()
