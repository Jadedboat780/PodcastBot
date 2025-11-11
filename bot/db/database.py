from beanie import init_beanie
from pymongo import AsyncMongoClient

from bot.config import config

from .models import AudioDoc


async def init_db():
    """Initialize the database"""

    client = AsyncMongoClient(config.mongo_url)
    await init_beanie(database=client.db_name, document_models=[AudioDoc])
