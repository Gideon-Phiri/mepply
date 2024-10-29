import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file


print("ALLOWED_FILE_TYPES:", os.getenv("ALLOWED_FILE_TYPES"))


class Settings(BaseSettings):
    """
    Application configuration settings loaded from environment variables.
    """
    database_url: str = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
    google_cloud_credentials: str = os.getenv("GOOGLE_CLOUD_CREDENTIALS")
    dropbox_access_token: str = os.getenv("DROPBOX_ACCESS_TOKEN")
    storage_provider: str = os.getenv("STORAGE_PROVIDER", "gcp")
    auth_service_url: str = os.getenv("AUTH_SERVICE_URL")
    allowed_file_types: list[str] = os.getenv(
            "ALLOWED_FILE_TYPES", "pdf,doc,docx").split(',')
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", 5 * 1024 * 1024))


settings = Settings()
