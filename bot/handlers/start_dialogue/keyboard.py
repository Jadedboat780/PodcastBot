from enum import StrEnum, auto
from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
	from locales.stub import TranslatorRunner


class KeyboardCommand(StrEnum):
	"""Commands enum"""

	START = auto()
	HELP = auto()


def initial_buttons(command: KeyboardCommand, i18n: TranslatorRunner) -> list[list[InlineKeyboardButton]] | None:
	"""Returns the inline-buttons for the initial message"""

	button_start = InlineKeyboardButton(text=i18n.button.start(), callback_data="start")
	button_help = InlineKeyboardButton(text=i18n.button.help(), callback_data="help")
	button_source = InlineKeyboardButton(text=i18n.button.source(), url="https://github.com/Jadedboat780/PodcastBot.git")

	if command == KeyboardCommand.START:
		return [[button_help], [button_source]]
	elif command == KeyboardCommand.HELP:
		return [[button_start], [button_source]]
	else:
		return None
