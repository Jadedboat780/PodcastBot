from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from bot.config import config

from .models import AudioDoc


async def init():
	# Create Motor client
	client = AsyncIOMotorClient(config.MONGO_URL)

	# Init beanie with the Product document class
	await init_beanie(database=client.db_name, document_models=[AudioDoc])
