from pydantic_settings import BaseSettings  # ✅ correct for Pydantic v2


class Settings(BaseSettings):
    PROJECT_NAME: str = "FinChat"
    BACKEND_CORS_ORIGINS: list[str] = ["*"]  # allow all for dev
    API_V1_STR: str = "/api"
    HF_TOKEN: str | None = None
    HF_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.3"
    PORT: int = 8000

    class Config:
        env_file = ".env"  # your environment variables


settings = Settings()
