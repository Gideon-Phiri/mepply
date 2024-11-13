from pydantic import BaseModel, EmailStr


class EmailRequest(BaseModel):
    """Model for incoming email request payload."""

    recipient_email: EmailStr
    subject: str
    template_name: str
    context: dict
