from aiogram.types import InlineKeyboardButton
from enum import StrEnum, auto


class Command(StrEnum):
    """Commands enum"""
    start = auto()
    help = auto()


button_start = InlineKeyboardButton(text="Начальное сообщение ↩", callback_data="start")
button_help = InlineKeyboardButton(text="Помощь ⓘ", callback_data="help")
button_github = InlineKeyboardButton(text="Исходный код этого проекта 💾", url="https://github.com/Jadedboat780/PodcastBot.git")
button_author = InlineKeyboardButton(text="Автор бота 💬", url="https://t.me/Tokin_Nikita")
button_donate = InlineKeyboardButton(text="🍺")


def initial_buttons(command: Command) -> list[list[InlineKeyboardButton]]:
    """Returns the inline-buttons for the initial message"""
    if command == Command.start:
        return [[button_help], [button_github]]
    elif command == Command.help:
        return [[button_start], [button_github], [button_author]]
