import httpx
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from app.config import settings


security = HTTPBearer()


async def get_current_user(token: str = Depends(security)):
    """
    Validate the user's token with the auth-service API.
    Raises HTTP 401 if the token is invalid.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.auth_service_url}/verify-token",
            headers={"Authorization": f"Bearer {token.credentials}"}
        )
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid / expired token")
    return response.json().get("user_id")
