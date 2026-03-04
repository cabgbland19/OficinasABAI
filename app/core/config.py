from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: Literal["dev", "prod"] = "dev"
    database_url: str = "sqlite:///./data/app.db"
    jwt_secret_key: str = Field(default="dev-secret-change-me", min_length=16)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    admin_username: str = "admin"
    admin_password: str = "ChangeMe"
    admin_role: str = "admin"
    SCRAPE_ENABLED: bool = True
    SCRAPE_RUN_ON_STARTUP: bool = True
    SCRAPE_INTERVAL_SECONDS: int = Field(default=3600, ge=60)
    SCRAPE_SOURCE_URL: str = "https://www.abaigroup.com/donde-encontrarnos/"

settings = Settings()