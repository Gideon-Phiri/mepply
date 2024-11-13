from fastapi import APIRouter, HTTPException
from app.models.email import EmailRequest
from app.services.email_sender import send_email

router = APIRouter()

@router.post("/send-email")
async def send_email_endpoint(email_request: EmailRequest):
    """Endpoint to send an email."""
    success = await send_email(  # Awaiting send_email here
        email_request.recipient_email,
        email_request.subject,
        email_request.template_name,
        email_request.context
    )
    if success:
        return {"message": "Email sent successfully"}
    raise HTTPException(status_code=500, detail="Failed to send email")
