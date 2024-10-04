from motor.motor_asyncio import AsyncIOMotorClient

from bot.config import config
from .models import StorageModel


class MongoDB:
    __slots__ = ("client", "db", "collection")

    def __init__(self, db_name: str, collection_name: str):
        self.client = AsyncIOMotorClient(config.mongo_url)
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

    async def ping(self):
        """Pings connection to the database."""
        await self.client.admin.command("ping")

    async def get_doc(self, id: str):
        """Get document by id"""
        cursor = self.collection.find_one({"_id": id})
        doc = await cursor
        return doc

    async def get_all_doc(self):
        """Get all documents"""
        cursor = self.collection.find()
        docs = [doc["_id"] for doc in await cursor.to_list(None)]
        return docs

    async def insert_doc(self, doc: StorageModel):
        """Insert document"""
        await self.collection.insert_one(doc.to_mongo())

    async def delete_doc(self, id: str):
        """Delete document by id"""
        result = await self.collection.delete_one({"_id": id})
        if result.deleted_count == 0:
            raise ValueError(f"Document with id {id} not found")


mongo_db = MongoDB(config.mongo_db_name, config.mongo_collection_name)
