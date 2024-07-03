from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    token: str
    admin_id: int

    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str

    model_config = SettingsConfigDict(env_file="../.env")

config = Config()