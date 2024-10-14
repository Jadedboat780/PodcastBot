from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
	"""Configuration environment variables"""

	token: str
	admin_id: int

	mongo_url: str
	mongo_db_name: str
	mongo_collection_name: str

	access_key: str
	secret_key: str
	endpoint_url: str
	bucket_name: str
	storage_path: str

	model_config = SettingsConfigDict(env_file=".env")


config = Config()
