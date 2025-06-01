import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fluentogram import TranslatorHub

from bot.config import config
from bot.db import init_db
from bot.handlers import start_router, support_router, url_router
from bot.middlewares import TranslatorRunnerMiddleware
from bot.utils import bot_menu, create_translator_hub


async def main():
	"""Entry point"""

	await init_db()

	bot = Bot(token=config.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
	dp = Dispatcher()
	translator_hub: TranslatorHub = create_translator_hub()

	dp.startup.register(bot_menu)
	dp.include_routers(start_router, support_router, url_router)
	dp.update.middleware(TranslatorRunnerMiddleware())
	await bot.delete_webhook(drop_pending_updates=True)

	await dp.start_polling(bot, _translator_hub=translator_hub, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())
