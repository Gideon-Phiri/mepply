# Asynchronous email send task using Celery.

from celery import Celery
from app.services.email_sender import send_email
from app.config import settings

celery_app = Celery('email_service', broker=settings.redis_uri)


@celery_app.task
def send_email_task(
                    recipient_email: str,
                    subject: str,
                    template_name: str,
                    context: dict):
    """Celery task to send email asynchronously.

    Args:
        recipient_email (str): Recipient's email address.
        subject (str): Subject of the email.
        template_name (str): Template file name.
        context (dict): Data context for template rendering.
    """
    return send_email(recipient_email, subject, template_name, context)
