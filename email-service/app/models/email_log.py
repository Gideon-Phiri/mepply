# app/models/email_log.py
from pydantic import BaseModel, EmailStr
from datetime import datetime


class EmailLog(BaseModel):
    """Schema for logging sent emails in MongoDB."""

    recipient_email: EmailStr
    subject: str
    status: str  # "sent" or "failed"
    timestamp: datetime
    message_id: str = None  # Optional message ID from the mail server
