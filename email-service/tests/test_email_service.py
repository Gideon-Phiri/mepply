from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_send_email():
    response = client.post(
        "/email/send-email",
        json={"to": "recipient@example.com", "subject": "Test", "body": "Hello, World!"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Email sent successfully"}
