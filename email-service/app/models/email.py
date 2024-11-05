"""Data models for email operations."""

from pydantic import BaseModel, EmailStr


class EmailRequest(BaseModel):
    """Model representing the data needed to send an email."""

    to: EmailStr
    subject: str
    body: str
