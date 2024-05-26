import logging
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.template.loader import get_template
from ninja import UploadedFile

from src.data.managers.task_manager import TaskManager

logger = logging.getLogger(__name__)


celery_manager = TaskManager(queue="tasks")


@celery_manager.add_task()
def change_file_content_type_task(
    file: UploadedFile, new_content_type: str = None
) -> UploadedFile:
    if new_content_type is None:
        new_content_type = "image/webp"
    file.content_type = new_content_type
    logger.info("File content type changed to %s", new_content_type)
    return file


@celery_manager.add_task()
def change_file_name_task(file: UploadedFile, new_name: str) -> UploadedFile:
    file.name = new_name
    logger.info("File name changed to %s", new_name)
    return file


@celery_manager.add_task()
def render_html_task(template_name: str, context: dict) -> dict:
    context = context or {}
    html_template = get_template(f"{template_name}.html")
    html_content = html_template.render(context)

    logger.info("HTML content rendered")
    return {"html_type": "html", "html_content": html_content}


@celery_manager.add_task()
def attach_files_task(msg_as_str: str, files: list) -> str:
    msg = MIMEMultipart("alternative")
    msg.attach(MIMEText(msg_as_str, _subtype="html"))

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
                    logger.info("File attached: %s", filename)
        except FileNotFoundError:
            logger.error(f"File not found: {filename}")
        except Exception as e:
            logger.error(f"Error attaching file {filename}: {str(e)}")
    return msg.as_string()
