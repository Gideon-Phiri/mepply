# test_auth_service.py
from app.services.auth_service import verify_user

# Replace with a valid token for testing
test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3MzViOGY1MGUwY2VkOWUzNGYxYmU1MCIsImlhdCI6MTczMTU3NTY2MSwiZXhwIjoxNzMxNTc5MjYxfQ.mRgUeWMKLi2T5yW2bPTO-oIzeLk1dvJD7Rbwe2kpwh8"

user_id = verify_user(test_token)
print("User ID:", user_id)
