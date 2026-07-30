from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Config(BaseSettings):
    # Telegram API
    telegram_api_id: int
    telegram_api_hash: str
    
    # PostgreSQL
    db_user: str
    db_password: str
    db_name: str
    test_db_name: str
    
    database_url: str
    test_database_url: str
    
    # Redis
    redis_password: str
    redis_url: str
    test_redis_url: str
    
    # Application Settings
    target_channel: str = "silkroadcargo"
    debug: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


config = Config()