# backend/app/core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinChat"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    API_V1_STR: str = "/api"

    # ✅ Add these two lines for OpenAI integration
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    class Config:
        env_file = ".env"  # tells Pydantic to load from .env file


settings = Settings()
