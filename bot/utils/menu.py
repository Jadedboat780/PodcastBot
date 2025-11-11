from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def bot_menu(bot: Bot) -> None:
    """Returns the buttons for the menu"""

    start_command = BotCommand(command="/start", description="Get the started message")
    faq_command = BotCommand(command="/help", description="How to use the bot")
    support_command = BotCommand(command="/support", description="Contact support")

    menu_commands = [
        start_command,
        faq_command,
        support_command,
    ]
    await bot.set_my_commands(menu_commands, BotCommandScopeDefault())
