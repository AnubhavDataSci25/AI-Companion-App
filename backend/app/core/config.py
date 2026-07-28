from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")

    app_name: str = "Ami Backend"
    database_url: str = "postgresql://companion_user:companion_pass@localhost:5433/companion_db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "changeme"
    GEMINI_API_KEY: str = ""


settings = Settings()
