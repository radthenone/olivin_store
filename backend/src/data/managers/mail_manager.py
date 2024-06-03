import logging
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

from django.conf import settings
from django.template.loader import get_template

from src.data.clients import MailClient

logger = logging.getLogger(__name__)


class MailManager:
    def __init__(self, client: MailClient = MailClient()):
        self.client = client

    @staticmethod
    def _render_html(template_name: str, context: Optional[dict]) -> str:
        context = context or {}
        html_template = get_template(f"{template_name}.html")
        html_content = html_template.render(context)

        logger.info("HTML content rendered")
        return html_content

    @staticmethod
    def _attach_files(msg: MIMEMultipart, files: List[str]) -> None:
        for filename in files:
            try:
                with open(filename, "rb") as file:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={filename}",
                    )
                    msg.attach(part)
                    logger.info("File attached: %s", filename)
            except FileNotFoundError:
                logger.error(f"File not found: {filename}")
            except Exception as e:
                logger.error(f"Error attaching file {filename}: {str(e)}")

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
        smtp = self.client.connect()
        if not smtp:
            if not fail_silently:
                raise smtplib.SMTPException("Failed to connect to the SMTP server")
            return False
        try:
            html_content = self._render_html(template_name, context)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = from_email
            msg["To"] = ", ".join(to_email)
            msg.attach(MIMEText(html_content, "html"))

            if files:
                self._attach_files(msg, files)

            smtp.sendmail(from_email, to_email, msg.as_string())
            logger.info("Successfully sent email")
            return True

        except smtplib.SMTPException as error:
            logger.error(f"Failed to send email: {str(error)}")
            if not fail_silently:
                raise
            return False
        finally:
            self.client.disconnect()
