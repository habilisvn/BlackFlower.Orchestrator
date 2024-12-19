from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # PostgreSQL configuration
    postgresql_prefix_async: str
    postgresql_prefix_sync: str
    postgresql_db_name: str
    postgresql_username: str
    postgresql_password: str
    postgresql_host: str
    postgresql_port: int

    # MongoDB configuration
    mongo_prefix: str
    mongo_db_name: str
    mongo_username: str
    mongo_password: str
    mongo_host: str
    mongo_port: int

    # JWT configuration
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    jwt_refresh_token_expire_days: int

    # Hugging Face API Key
    huggingface_api_key: str
    huggingface_transcribe_url: str

    # OpenAI API Key
    openai_api_key: str

    def __new__(cls, env_file: str = ".env", *args, **kwargs):
        cls.model_config = SettingsConfigDict(env_file=env_file)
        instance = super().__new__(cls, *args, **kwargs)
        return instance


@lru_cache
def get_settings():
    return Settings()  # type: ignore
