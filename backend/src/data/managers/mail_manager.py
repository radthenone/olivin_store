import logging
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from src.data.clients import MailClient

logger = logging.getLogger(__name__)


class MailManager:
    def __init__(
        self,
        client: MailClient = MailClient(),
    ):
        self.client = client
        self.smtp = self.client.connect()

    @staticmethod
    def _get_template(template_name: str):
        return get_template(f"{template_name}.html")

    @staticmethod
    def _attach_files(msg: MIMEMultipart, files: list[str]) -> None:
        for filename in files:
            try:
                with open(filename, "rb") as file:
                    file_data = file.read()
                    if file_data:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(file_data)
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={filename}",
                        )
                        msg.attach(part)
            except FileNotFoundError:
                logger.error(f"File not found: {filename}")
            except Exception as e:
                logger.error(f"Error attaching file {filename}: {str(e)}")

    @classmethod
    def _render_html(cls, template_name: str, context: dict) -> tuple[str, str]:
        html_type = "html"
        context = context or {}
        html_template = cls._get_template(template_name=template_name)
        return html_type, html_template.render(Context(context))

    def send_mail(
        self,
        subject: str,
        to_email: list,
        template_name: str,
        context: Optional[dict] = None,
        from_email: str = settings.EMAIL_HOST_USER,
        files: Optional[list] = None,
        fail_silently: bool = False,
    ):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = ", ".join(to_email)

        html_type, html_content = self._render_html(
            template_name=template_name, context=context
        )
        msg.attach(MIMEText(html_content, _subtype=html_type))

        if files:
            self._attach_files(msg, files)

        try:
            self.smtp.sendmail(from_email, to_email, msg.as_string())
            logger.info("Successfully sent email")
        except smtplib.SMTPException as error:
            logger.error(f"Failed to send email: {str(error)}")
            if not fail_silently:
                raise
        finally:
            self.client.disconnect()
