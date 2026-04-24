"""
Application configuration
Environment variables and settings management
"""


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

    # API Configuration
    PROJECT_NAME: str = "DevSecOps Social App API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = ""  # loaded from .env

    # Security - JWT Tokens
    SECRET_KEY: str = ""  # loaded from .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Security - Sessions
    SESSION_SECRET_KEY: str = ""  # loaded from .env
    SESSION_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://discsecops.github.io"
    ]

    # Environment
    ENVIRONMENT: str = "development"  # overridden in production
    FRONTEND_URL: str = "http://localhost:3000"  # used for CSP


# Global settings instance
settings = Settings()
