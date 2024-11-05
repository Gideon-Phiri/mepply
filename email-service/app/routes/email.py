"""API routes for handling email operations."""

from fastapi import APIRouter, HTTPException
from app.models.email import EmailRequest
from app.services.email_sender import send_email

router = APIRouter()


@router.post("/send-email")
async def send_email_endpoint(email_request: EmailRequest):
    """Endpoint to send an email.

    Args:
        email_request (EmailRequest): The email request details.

    Returns:
        dict: Success message if email is sent.
    Raises:
        HTTPException: If the email sending fails.
    """
    if send_email(email_request):
        return {"message": "Email sent successfully"}
    raise HTTPException(status_code=500, detail="Failed to send email")
