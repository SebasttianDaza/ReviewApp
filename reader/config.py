from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    mongo_uri: str
    redis_cache_host_reader: str
    redis_cache_port_reader: int
    redis_cache_master_node_reader: str
    redis_cache_username_reader: str
    redis_cache_password_reader: str
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()