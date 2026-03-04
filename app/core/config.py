from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal

class Settings(BaseSettings):
    environment: Literal["dev", "prod"] = "dev"

    database_url: str = "sqlite:///./data/app.db"

    jwt_secret_key: str = Field(default="dev-secret-change-me", min_length=16)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    admin_username: str = "admin"
    admin_password: str = "ChangeMe_123!"
    admin_role: str = "admin"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()