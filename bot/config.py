from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
	"""Configuration environment variables"""

	token: str
	admin_id: int

	mongo_host: str

	access_key: str
	secret_key: str
	endpoint_url: str
	bucket_name: str
	domain: str

	@property
	def MONGO_URL(self) -> str:
		return f"mongodb://{self.mongo_host}:27017"

	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
