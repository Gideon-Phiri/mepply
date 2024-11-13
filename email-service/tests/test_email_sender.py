import pytest
from unittest.mock import patch, MagicMock
from app.services.email_sender import send_email

@pytest.mark.asyncio
async def test_send_email_success():
    """Test the send_email function with a successful response."""
    with patch("smtplib.SMTP", autospec=True) as mock_smtp, \
         patch("app.services.email_sender.load_template", return_value="<html>Email Content</html>"):

        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.sendmail = MagicMock(return_value={})  # Mock sendmail

        result = await send_email(  # Awaiting send_email here
            recipient_email="test@example.com",
            subject="Test Subject",
            template_name="verification_email.html",
            context={"user_name": "Test User", "verification_code": "123456"}
        )

        # Assert sendmail was called once
        mock_smtp_instance.sendmail.assert_called_once()
        assert result is True  # Checking the function returns True on success
