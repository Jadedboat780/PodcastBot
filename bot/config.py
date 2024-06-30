from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    token: str
    admin_id: int

    model_config = SettingsConfigDict(env_file="../.env")