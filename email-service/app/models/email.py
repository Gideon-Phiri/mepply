"""Data models for email operations."""

from datetime import datetime
from pydantic import BaseModel, EmailStr
from mongoengine import Document, StringField, DateTimeField, EmailField


class EmailRequest(BaseModel):
    """Model representing the data needed to send an email."""

    to: EmailStr
    subject: str
    body: str


class EmailLog(Document):
    """MongoDB model to log emails sent through the email service."""
    recipient = EmailField(required=True)
    subject = StringField(required=True)
    status = StringField(required=True, choices=('sent', 'failed'))
    error = StringField()
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'email_logs'  # MongoDB collection name
    }

    @classmethod
    def log_email(cls, recipient, subject, status, error=None):
        cls.collection.insert_one({
            "recipient": recipient,
            "subject": subject,
            "status": status,
            "error": error,
            "timestamp": datetime.utcnow(),
        })
