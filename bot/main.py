from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import asyncio

from bot.handlers import start_router, url_router
from bot.keyboards import main_menu
from bot.config import config


async def main():
    """Entry point"""
    bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.startup.register(main_menu)
    dp.include_routers(start_router, url_router)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
