import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config
from bot.db import init_db
from bot.handlers import handlers
from bot.middlewares import TranslatorRunnerMiddleware
from bot.utils import bot_menu, create_translator_hub


async def main():
    """Entry point"""

    # Initialize the database, bot and dispatcher
    await init_db()
    bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Register menu, routers and  middleware
    dp.startup.register(bot_menu)
    dp.include_routers(*handlers)
    dp.update.middleware(TranslatorRunnerMiddleware())

    # Deleting messages received while the bot was not working
    await bot.delete_webhook(drop_pending_updates=True)

    # Start polling
    await dp.start_polling(bot, _translator_hub=create_translator_hub(), allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
