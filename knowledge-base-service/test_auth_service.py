# test_auth_service.py
from app.services.auth_service import verify_user

# Replace with a valid token for testing
test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3MzQzNmM1ODBjMmI0YzBiMmFhY2U1NyIsImlhdCI6MTczMTUwNjgzNiwiZXhwIjoxNzMxNTEwNDM2fQ.JdNNgwXDjqdBQCWhhouXyYdv2L3ilHQ1kR8xAJqtSDo"

user_id = verify_user(test_token)
print("User ID:", user_id)
