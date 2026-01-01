"""
Configuration management using pydantic-settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Database
    neon_database_url: str

    # Authentication
    auth_secret: str
    session_duration_days: int = 7

    # CORS
    frontend_url: str = "http://localhost:3000"

    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False  # Must be False in production

    # Environment
    environment: str = "development"
    log_level: str = "info"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
