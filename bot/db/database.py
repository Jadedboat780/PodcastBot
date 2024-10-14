from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from bot.config import config

from .models import AudioDoc, Document


class MongoCollection:
	__slots__ = ("client", "db", "collection")

	def __init__(self, db_name: str, collection_name: str):
		self.client = AsyncIOMotorClient(
			config.mongo_url, minPoolSize=5, maxPoolSize=20, maxIdleTimeMS=10000, socketTimeoutMS=5000, connectTimeoutMS=2000
		)
		self.db = self.client.get_database(db_name)
		self.collection = self.db.get_collection(collection_name)

	async def ping(self) -> bool:
		"""Pings the database to check if the connection is alive"""
		try:
			await self.client.admin.command("ping")
			return True
		except ServerSelectionTimeoutError:
			return False

	async def get_doc(self, params: dict[str:any]) -> Document | AudioDoc | None:
		"""Get a document by parameters"""
		doc = await self.collection.find_one(params)
		if not doc:
			return None

		return Document.to_model(doc)

	async def get_all_docs(self) -> list[Document | AudioDoc]:
		"""Get all documents"""
		docs = []
		cursor = self.collection.find()
		async for doc in cursor:
			docs.append(doc)

		return docs

	async def insert_doc(self, doc: Document | AudioDoc) -> None:
		"""Insert document"""
		await self.collection.insert_one(doc.to_mongo())

	async def delete_doc(self, params: dict[str:any]) -> None:
		"""Delete document by parameters"""
		result = await self.collection.delete_one(params)
		if result.deleted_count == 0:
			raise ValueError(f"The document with parameters '{params}' was not found")

	def __repr__(self):
		return f"MongoDB(db={self.db.name}, collection={self.collection.name})"


mongo_collection = MongoCollection(config.mongo_db_name, config.mongo_collection_name)
