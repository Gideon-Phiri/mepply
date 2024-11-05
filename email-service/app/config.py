# pylint: disable=too-few-public-methods
"""Configuration for environment variables and settings."""

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    """Settings for environment variables and email configuration."""
    email_host: str
    email_port: int = 587
    email_user: str
    email_password: str

    class Config:
        """Config class for environment variables."""
        env_file = ".env"


settings = Settings()
