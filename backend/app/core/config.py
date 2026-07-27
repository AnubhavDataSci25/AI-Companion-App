from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Ami Backend"
    database_url: str = "postgresql://companion_user:companion_pass@localhost:5432/companion_db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "changeme"

    class Config:
        env_file = ".env"


settings = Settings()