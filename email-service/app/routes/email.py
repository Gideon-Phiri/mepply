from fastapi import APIRouter, HTTPException
from app.models.email import EmailRequest
from app.services.email_sender import send_email


router = APIRouter()


@router.post("/send-email")
async def send_email_endpoint(email_request: EmailRequest):
    if send_email(email_request):
        return {"message": "Email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")
