import smtplib
from email.mime.text import MIMEText
from app.config import settings
from app.models.email import EmailRequest

def send_email(email_request: EmailRequest) -> bool:
    """Send an email based on the provided EmailRequest object."""
    msg = MIMEText(email_request.body)
    msg["Subject"] = email_request.subject
    msg["From"] = settings.email_user
    msg["To"] = email_request.to

    try:
        with smtplib.SMTP(settings.email_host, settings.email_port) as server:
            server.starttls()
            server.login(settings.email_user, settings.email_password)
            server.sendmail(settings.email_user, email_request.to, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
