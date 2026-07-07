from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    telegram_api_id: int
    telegram_api_hash: str
    database_url: str
    
    target_channel: str = "silkroadcargo"
    debug: bool = True
    
    model_config = SettingsConfigDict(env_file=".env")

config = Config()