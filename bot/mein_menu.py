from aiogram import Bot
from aiogram.types import BotCommand


async def main_menu(bot: Bot) -> None:
	"""Returns the buttons for the main menu"""
	start_command = BotCommand(command="/start", description="Начальное сообщение")
	menu_commands = [
		start_command,
	]
	await bot.set_my_commands(menu_commands)
