from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
 
 
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Gemini
    gemini_api_key: str
    model: str = "gemini-2.5-flash"
    max_tokens: int = 1024
 
    # API
    app_version: str = "0.1.0"
    environment: Literal["development", "production"] = "development"
    rate_limit: str = "30/minute"  # SlowAPI format
 
    # Logging
    log_level: str = "INFO"
 
 
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]