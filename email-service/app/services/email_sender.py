import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import settings
from app.utils.template_loader import load_template
from datetime import datetime
from app.models.email_log import EmailLog
from motor.motor_asyncio import AsyncIOMotorClient


# Initialize MongoDB client
client = AsyncIOMotorClient(settings.mongodb_uri)
db = client.email_service_db
email_logs = db.email_logs


async def send_email(
                     recipient_email: str,
                     subject: str,
                     template_name: str,
                     context: dict) -> bool:
    """Send an email and log the result in MongoDB.

    Args:
        recipient_email (str): Recipient email address.
        subject (str): Subject of the email.
        template_name (str): Template file name.
        context (dict): Data context for rendering the template.

    Returns:
        bool: True if email is sent successfully, False otherwise.
    """
    try:
        # Create email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.sender_email
        msg["To"] = recipient_email
        html_content = load_template(template_name, context)
        msg.attach(MIMEText(html_content, "html"))

        # Connect to SMTP and send email
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_username, settings.smtp_password)
            server.sendmail(settings.sender_email, recipient_email, msg.as_string())

        # Log successful send to MongoDB
        await email_logs.insert_one(EmailLog(
            recipient_email=recipient_email,
            subject=subject,
            status="sent",
            timestamp=datetime.utcnow()
        ).model_dump())
        return True

    except Exception as e:
        # Log failed send to MongoDB
        await email_logs.insert_one(EmailLog(
            recipient_email=recipient_email,
            subject=subject,
            status="failed",
            timestamp=datetime.utcnow()
        ).model_dump())
        print(f"Failed to send email: {e}")
        return False
