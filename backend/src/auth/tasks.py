import logging

from celery.exceptions import MaxRetriesExceededError

from src.core.celery import celery
from src.data.clients import MailClient
from src.data.handlers import RegistrationEmailHandler
from src.data.managers import MailManager

logger = logging.getLogger(name="celery")
logger.setLevel(logging.DEBUG)


@celery.task(queue="tasks")
def send_registration_email_task(url: str, image: str, email: str):
    logger.info("Sending registration email")
    try:
        mail_handler = RegistrationEmailHandler(
            manager=MailManager(client=MailClient())
        )
    except Exception as error:
        logger.error(f"Failed to initialize mail handler: {str(error)}")
        raise Exception("Failed to initialize mail handler")
    mail_handler.send_registration_email(
        to_email=email, context={"url": url, "image": image}
    )
    logger.info("Registration email sent")
