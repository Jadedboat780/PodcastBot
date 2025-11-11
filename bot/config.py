from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Configuration environment variables"""

    token: str
    admin_id: int

    mongo_username: str
    mongo_password: str
    mongo_database: str
    mongo_host: str
    mongo_port: int
    mongo_auth_db: str

    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str
    domain: str

    @property
    def mongo_url(self) -> str:
        return f"mongodb://{self.mongo_username}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/{self.mongo_database}?authSource={self.mongo_auth_db}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
