from enum import StrEnum, auto

from aiogram.types import InlineKeyboardButton


class Command(StrEnum):
	"""Commands enum"""

	START = auto()
	HELP = auto()


button_start = InlineKeyboardButton(text="Начальное сообщение ↩", callback_data="start")
button_help = InlineKeyboardButton(text="Помощь ⓘ", callback_data="help")
button_github = InlineKeyboardButton(text="Исходный код этого проекта 💾", url="https://github.com/Jadedboat780/PodcastBot.git")
button_author = InlineKeyboardButton(text="Автор бота 💬", url="https://t.me/Tokin_Nikita")


def initial_buttons(command: Command) -> list[list[InlineKeyboardButton]] | None:
	"""Returns the inline-buttons for the initial message"""
	if command == Command.START:
		return [[button_help], [button_github]]
	elif command == Command.HELP:
		return [[button_start], [button_github], [button_author]]
	else:
		return None
