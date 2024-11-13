# pylint: disable=too-few-public-methods
"""Configuration for environment variables and settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class Settings(BaseSettings):
    """Settings for environment variables and email configuration."""
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    sender_email: EmailStr
    smtp_use_tls: bool

    # Mongodb Configuration
    mongodb_uri: str

    # Redis server configuration
    redis_uri: str

    #Email Service API Configurations
    email_service_api_key: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
