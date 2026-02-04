from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    Settings are loaded from environment variables or a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )  # read settings from .env file

    DATABASE_URL: str = "postgresql+asyncpg://user:password@db/app_db"
    # Default to the dev container's local PostgreSQL for development.
    # When deploying to a cloud provider like Neon, this variable will be
    # overridden by the environment variable provided by the hosting service.


settings = Settings()
