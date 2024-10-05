from motor.motor_asyncio import AsyncIOMotorClient

from .models import Document
from bot.config import config


class MongoCollection:
    __slots__ = ("client", "db", "collection")

    def __init__(self, db_name: str, collection_name: str):
        self.client = AsyncIOMotorClient(
            config.mongo_url,
            minPoolSize=5,
            maxPoolSize=20,
            maxIdleTimeMS=10000,
            socketTimeoutMS=5000,
            connectTimeoutMS=2000
        )
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

    async def ping(self) -> bool:
        """Pings the database to check if the connection is alive"""
        try:
            await self.client.admin.command("ping")
            return True
        except:
            return False

    async def get_doc(self, id: str) -> Document | None:
        """Get a document by id"""
        doc = await self.collection.find_one({"_id": id})
        return doc

    async def get_all_doc(self) -> list[Document]:
        """Get all documents"""
        docs = []
        cursor = self.collection.find()
        async for doc in cursor:
            docs.append(doc)

        return docs

    async def insert_doc(self, doc: Document) -> None:
        """Insert document"""
        await self.collection.insert_one(doc.to_mongo())

    async def delete_doc(self, id: str) -> None:
        """Delete document by id"""
        result = await self.collection.delete_one({"_id": id})
        if result.deleted_count == 0:
            raise ValueError(f"Document with id {id} not found")

    def __repr__(self):
        return f'MongoDB(db={self.db.name}, collection={self.collection.name})'


mongo_collection = MongoCollection(config.mongo_db_name, config.mongo_collection_name)
