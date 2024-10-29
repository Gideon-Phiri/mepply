from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


client = AsyncIOMotorClient(settings.database_url)
db = client.knowledge_base_service
