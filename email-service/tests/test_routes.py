from fastapi.testclient import TestClient
from app.app import apptest_routes.py
from app.config import settings

client = TestClient(app)


def test_send_email_endpoint():
    """Test the /send-email endpoint with valid data."""
    response = client.post(
        "/send-email",
        headers={"x-api-key": settings.email_service_api_key},
        json={
            "recipient_email": "test@example.com",
            "subject": "Test Email",
            "template_name": "verification_email.html",
            "context": {"user_name": "Test User", "verification_code": "123456"}
        }
    )
    assert response.status_code == 202
    assert response.json()["status"] == "Email is being sent"
