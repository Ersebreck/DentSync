"""
Application settings management using Pydantic.
This module handles all configuration settings for the dental clinic system,
including database connections, API settings, and security configurations.
"""

from typing import Any, Dict, Optional
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, validator
import secrets

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DentSync"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database Configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "dentsync"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """
        Constructs the database URL from individual components if not provided directly.
        This allows for flexible configuration through environment variables.
        """
        if isinstance(v, str):
            return v
            
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}"
        )

    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = ["http://localhost:8000", "http://localhost:3000"]

    class Config:
        case_sensitive = True
        env_file = ".env"

# Create a global settings instance
settings = Settings()